from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from PIL import Image

from apps.core.models import Contact
from apps.plants.management.commands.replace_plant_photos import Command, is_managed_cover
from apps.plants.models import Plant, Comment, PhotoImportProgress, PlantImage


User = get_user_model()


class PhotoImportTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.plant = Plant.objects.create(
            name="Cucumber", category=Plant.Category.VEGETABLE,
            image="plants/covers/seed-cucumber.jpg",
            managed_cover_path="plants/covers/seed-cucumber.jpg",
        )
        cls.photos = [
            {
                "title": f"File:{name}.jpg", "url": f"https://example.test/{name}.jpg",
                "source": f"https://example.test/wiki/{name}", "author": "Photographer",
                "license": "CC BY 4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
            }
            for name in ("cover", "detail")
        ]

    def setUp(self):
        media = TemporaryDirectory()
        self.addCleanup(media.cleanup)
        self.media = Path(media.name)
        settings = self.settings(MEDIA_ROOT=self.media)
        settings.enable()
        self.addCleanup(settings.disable)
        self.command = Command()

    def test_failed_gallery_download_leaves_plant_and_media_untouched(self):
        with patch.object(self.command, "download_image", side_effect=[b"cover", ValueError("gallery")]):
            with self.assertRaisesMessage(ValueError, "gallery"):
                self.command.import_plant(None, self.plant, self.photos, "a" * 64, [])
        self.plant.refresh_from_db()
        self.assertEqual(self.plant.image.name, "plants/covers/seed-cucumber.jpg")
        self.assertFalse(self.plant.images.exists())
        self.assertFalse(PhotoImportProgress.objects.exists())
        self.assertFalse(any(path.is_file() for path in self.media.rglob("*")))

    def test_manual_cover_changed_during_download_is_preserved(self):
        manual_path = "plants/covers/commons-manual.jpg"

        def download(session, url):
            Plant.objects.filter(pk=self.plant.pk).update(
                image=manual_path, managed_cover_path="",
            )
            return b"validated"

        with patch.object(self.command, "download_image", side_effect=download):
            with self.assertRaisesMessage(ValueError, "changed during download"):
                self.command.import_plant(None, self.plant, self.photos, "a" * 64, [])
        self.plant.refresh_from_db()
        self.assertEqual(self.plant.image.name, manual_path)
        self.assertFalse(self.plant.images.exists())
        self.assertFalse(PhotoImportProgress.objects.exists())
        self.assertFalse(any(path.is_file() for path in self.media.rglob("*")))

    def test_retry_queue_prioritizes_unattempted_selections(self):
        second = Plant.objects.create(
            name="Eggplant", category=Plant.Category.VEGETABLE,
            image="plants/covers/seed-eggplant.jpg",
            managed_cover_path="plants/covers/seed-eggplant.jpg",
        )
        manifest = {self.plant.pk: self.photos, second.pk: self.photos}
        rows = [
            {"plant_id": str(plant_id), "cover_index": "0", "gallery_indices": "1"}
            for plant_id in manifest
        ]
        pending, _ = self.command.pending_selections(manifest, rows)
        self.assertEqual([entry[0].pk for entry in pending], [self.plant.pk, second.pk])
        PhotoImportProgress.objects.create(plant=self.plant, fingerprint=pending[0][2])
        pending, _ = self.command.pending_selections(manifest, rows)
        self.assertEqual([entry[0].pk for entry in pending], [second.pk, self.plant.pk])

    def test_database_failure_rolls_back_cover_gallery_and_new_files(self):
        with (
            patch.object(self.command, "download_image", return_value=b"validated"),
            patch.object(PlantImage, "save", side_effect=ValueError("gallery write")),
        ):
            with self.assertRaisesMessage(ValueError, "gallery write"):
                self.command.import_plant(None, self.plant, self.photos, "a" * 64, [])
        self.plant.refresh_from_db()
        self.assertEqual(self.plant.image.name, "plants/covers/seed-cucumber.jpg")
        self.assertFalse(self.plant.images.exists())
        self.assertFalse(PhotoImportProgress.objects.exists())
        self.assertFalse(any(path.is_file() for path in self.media.rglob("*")))

    def test_completed_selection_is_skipped_and_credits_resume_from_database(self):
        gallery = PlantImage.objects.create(
            plant=self.plant, image="plants/gallery/manual.jpg", position=7,
        )
        rows = [{"plant_id": str(self.plant.pk), "cover_index": "0", "gallery_indices": "1"}]
        manifest = {self.plant.pk: self.photos}
        pending, _ = self.command.pending_selections(manifest, rows)
        plant, photos, fingerprint = pending[0]
        legacy = dict(plant_id=str(plant.pk), role="gallery", image_file=gallery.image.name,
                      source="manual", custom_note="retain this field")
        credits_path = self.media / "credits.csv"
        with (
            patch("apps.plants.management.commands.replace_plant_photos.CREDITS", credits_path),
            patch.object(self.command, "download_image", return_value=b"validated"),
        ):
            self.command.save_credits([legacy])
            self.command.import_plant(None, plant, photos, fingerprint, [legacy])
            self.assertEqual(self.command.pending_selections(manifest, rows), ([], 0))
            self.assertEqual(len(self.command.load_credits()), 1)
            synced = self.command.sync_credits()
            self.assertEqual(len(synced), 3)
            self.assertEqual(self.command.sync_credits()[0]["custom_note"], "retain this field")
            self.assertEqual(len(self.command.load_credits()), 3)
        self.assertEqual(list(plant.images.values_list("position", flat=True)), [7, 8])


def test_image(name="test.jpg"):
    image = Image.new("RGB", (100, 100), "green")
    buffer = BytesIO()
    image.save(buffer, format="JPEG")

    return SimpleUploadedFile(
        name,
        buffer.getvalue(),
        content_type="image/jpeg",
    )


class PlanteerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="owner",
            password="TestPass123!",
        )

        cls.other = User.objects.create_user(
            username="other",
            password="TestPass123!",
        )

        cls.staff = User.objects.create_user(
            username="staff",
            password="TestPass123!",
            is_staff=True,
        )

        cls.plant = Plant.objects.create(
            name="Rose",
            about="Beautiful flowering plant",
            used_for="Decoration",
            image="plants/covers/rose.jpg",
            category=Plant.Category.FLOWER,
            is_edible=False,
            created_by=cls.owner,
        )

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_manual_cover_uploads_with_managed_prefixes_are_protected(self):
        plant = self.plant
        with TemporaryDirectory() as media_root, self.settings(MEDIA_ROOT=media_root):
            for filename in ("seed-rose.jpg", "commons-cover-rose.jpg"):
                with self.subTest(filename=filename):
                    plant.image = f"plants/covers/{filename}"
                    plant.managed_cover_path = plant.image.name
                    plant.save(update_fields=["image", "managed_cover_path"])
                    self.assertTrue(is_managed_cover(plant))

                    # With no preexisting file in storage the name can be reused.
                    plant.image = test_image(filename)
                    plant.save(update_fields=["image"])
                    plant.refresh_from_db()
                    self.assertEqual(plant.image.name, f"plants/covers/{filename}")
                    self.assertFalse(is_managed_cover(plant))

    def test_plants_page(self):
        response = self.client.get(reverse("plant_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rose")

    def test_plant_detail(self):
        response = self.client.get(
            reverse("plant_detail", args=[self.plant.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rose")

    def test_search(self):
        response = self.client.get(
            reverse("plant_search"),
            {"q": "Rose"},
        )
        self.assertContains(response, "Rose")

    def test_category_filter(self):
        response = self.client.get(
            reverse("plant_list"),
            {"category": "FLOWER"},
        )
        self.assertContains(response, "Rose")

    def test_contact_submission(self):
        response = self.client.post(
            reverse("contact"),
            {
                "first_name": "Ahmed",
                "last_name": "Ali",
                "email": "ahmed@example.com",
                "message": "Hello Planteer",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contact.objects.count(), 1)

    def test_anonymous_cannot_add_plant(self):
        response = self.client.get(reverse("plant_create"))
        self.assertEqual(response.status_code, 302)

    def test_owner_can_edit(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse("plant_update", args=[self.plant.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_edit(self):
        self.client.force_login(self.other)

        response = self.client.get(
            reverse("plant_update", args=[self.plant.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_other_user_cannot_delete(self):
        self.client.force_login(self.other)

        response = self.client.post(
            reverse("plant_delete", args=[self.plant.pk])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(
            Plant.objects.filter(pk=self.plant.pk).exists()
        )

    def test_staff_can_edit(self):
        self.client.force_login(self.staff)

        response = self.client.get(
            reverse("plant_update", args=[self.plant.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_dashboard_staff_only(self):
        self.client.force_login(self.owner)

        response = self.client.get(
            reverse("dashboard_home")
        )

        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.staff)

        response = self.client.get(
            reverse("dashboard_home")
        )

        self.assertEqual(response.status_code, 200)

    def test_add_comment(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("add_comment", args=[self.plant.pk]),
            {"content": "Amazing plant!"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_anonymous_cannot_comment(self):
        response = self.client.post(
            reverse("add_comment", args=[self.plant.pk]),
            {"content": "Anonymous comment"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    def test_gallery_creation(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("plant_create"),
            {
                "name": "Aloe Vera",
                "about": "A succulent plant",
                "used_for": "Skin care",
                "image": test_image("cover.jpg"),
                "category": "SUCCULENT",
                "is_edible": "",
                "images-TOTAL_FORMS": "1",
                "images-INITIAL_FORMS": "0",
                "images-MIN_NUM_FORMS": "0",
                "images-MAX_NUM_FORMS": "1000",
                "images-0-image": test_image("gallery.jpg"),
                "images-0-alt_text": "Aloe leaf",
                "images-0-position": "0",
            },
        )

        self.assertEqual(response.status_code, 302)

        plant = Plant.objects.get(name="Aloe Vera")

        self.assertEqual(
            PlantImage.objects.filter(plant=plant).count(),
            1,
        )

    def test_staff_deletes_comment(self):
        comment = Comment.objects.create(
            plant=self.plant,
            user=self.owner,
            content="Test comment",
        )

        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "dashboard_comment_delete",
                args=[comment.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Comment.objects.filter(pk=comment.pk).exists()
        )

    def test_regular_user_cannot_delete_comment(self):
        comment = Comment.objects.create(
            plant=self.plant,
            user=self.owner,
            content="Protected comment",
        )

        self.client.force_login(self.other)

        response = self.client.post(
            reverse(
                "dashboard_comment_delete",
                args=[comment.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(pk=comment.pk).exists()
        )

    def test_staff_deletes_message(self):
        contact = Contact.objects.create(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            message="Hello",
        )

        self.client.force_login(self.staff)

        response = self.client.post(
            reverse(
                "dashboard_message_delete",
                args=[contact.pk],
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Contact.objects.filter(pk=contact.pk).exists()
        )
