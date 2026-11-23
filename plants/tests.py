import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Comment, Plant


def make_plant(name="Mint", category=Plant.Category.HERB, is_edible=True):
    """Helper: create a plant quickly inside tests."""
    return Plant.objects.create(
        name=name,
        about=f"About {name}",
        used_for="Cooking",
        image="plants/test.jpg",
        category=category,
        is_edible=is_edible,
    )


def make_image_file(name="test.jpg"):
    """Helper: a tiny real JPEG image for upload tests."""
    buffer = BytesIO()
    Image.new("RGB", (10, 10), "green").save(buffer, format="JPEG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


# Uploaded test images go to a temporary folder, not the real media/ folder
TEMP_MEDIA = tempfile.mkdtemp()


class PlantModelTests(TestCase):
    def test_str_returns_name(self):
        self.assertEqual(str(make_plant(name="Basil")), "Basil")

    def test_comments_related_name_and_cascade(self):
        plant = make_plant()
        Comment.objects.create(plant=plant, full_name="Sara Ali", content="Lovely!")
        self.assertEqual(plant.comments.count(), 1)

        plant.delete()  # CASCADE should delete the comment too
        self.assertEqual(Comment.objects.count(), 0)


class PlantDetailTests(TestCase):
    def test_detail_page_loads(self):
        plant = make_plant(name="Olive Tree", category=Plant.Category.TREE)
        response = self.client.get(reverse("plants:plant_detail", args=[plant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Olive Tree")

    def test_detail_page_404_for_missing_plant(self):
        response = self.client.get(reverse("plants:plant_detail", args=[999]))
        self.assertEqual(response.status_code, 404)


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class PlantCrudTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)
        super().tearDownClass()

    def valid_data(self, **changes):
        data = {
            "name": "Lavender",
            "category": Plant.Category.FLOWER,
            "is_edible": "on",
            "about": "A fragrant purple flower.",
            "used_for": "Perfumes and tea.",
        }
        data.update(changes)
        return data

    # ----- Create -----
    def test_add_page_loads(self):
        response = self.client.get(reverse("plants:plant_create"))
        self.assertEqual(response.status_code, 200)

    def test_add_plant_with_valid_data(self):
        data = self.valid_data(image=make_image_file())
        response = self.client.post(reverse("plants:plant_create"), data, follow=True)

        plant = Plant.objects.get(name="Lavender")
        self.assertTrue(plant.is_edible)
        self.assertTrue(plant.image.name.startswith("plants/"))
        self.assertRedirects(response, reverse("plants:plant_detail", args=[plant.id]))
        self.assertContains(response, "was added successfully")

    def test_add_plant_rejects_empty_form(self):
        response = self.client.post(reverse("plants:plant_create"), {})
        self.assertEqual(response.status_code, 200)  # form shown again with errors
        self.assertEqual(Plant.objects.count(), 0)
        self.assertTrue(response.context["form"].errors)

    def test_add_plant_requires_image(self):
        self.client.post(reverse("plants:plant_create"), self.valid_data())
        self.assertEqual(Plant.objects.count(), 0)

    # ----- Update -----
    def test_update_page_is_prefilled(self):
        plant = make_plant(name="Mint")
        response = self.client.get(reverse("plants:plant_update", args=[plant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["form"].instance, plant)

    def test_update_plant_keeps_old_image(self):
        plant = make_plant(name="Mint")
        data = self.valid_data(name="Peppermint", category=Plant.Category.HERB)
        response = self.client.post(reverse("plants:plant_update", args=[plant.id]), data)

        plant.refresh_from_db()
        self.assertEqual(plant.name, "Peppermint")
        self.assertEqual(plant.image.name, "plants/test.jpg")  # not removed
        self.assertRedirects(response, reverse("plants:plant_detail", args=[plant.id]))

    def test_update_missing_plant_returns_404(self):
        response = self.client.get(reverse("plants:plant_update", args=[999]))
        self.assertEqual(response.status_code, 404)

    # ----- Delete -----
    def test_delete_get_shows_confirmation_and_does_not_delete(self):
        plant = make_plant()
        response = self.client.get(reverse("plants:plant_delete", args=[plant.id]))
        self.assertContains(response, "Delete Mint?")
        self.assertTrue(Plant.objects.filter(pk=plant.id).exists())

    def test_delete_post_deletes_plant(self):
        plant = make_plant()
        response = self.client.post(reverse("plants:plant_delete", args=[plant.id]))
        self.assertRedirects(response, reverse("main:home"))
        self.assertFalse(Plant.objects.filter(pk=plant.id).exists())
