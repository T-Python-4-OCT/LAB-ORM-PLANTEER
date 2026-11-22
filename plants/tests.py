from io import BytesIO, StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.contrib.staticfiles import finders
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from PIL import Image

from .models import Comment, Plant


class PlantTests(TestCase):
    def setUp(self):
        media = self.enterContext(TemporaryDirectory())
        self.enterContext(self.settings(MEDIA_ROOT=media))
        self.basil = Plant.objects.create(
            name="Sweet Basil", about="A fragrant annual.", used_for="Pesto and sauces.",
            category=Plant.Category.HERBS, image="plants/basil.webp", is_edible=True,
        )
        self.rosemary = Plant.objects.create(
            name="Rosemary", about="A Mediterranean herb.", used_for="Roasts.",
            category=Plant.Category.HERBS, image="plants/rosemary.webp", is_edible=True,
        )
        self.lavender = Plant.objects.create(
            name="Lavender", about="A fragrant shrub.", used_for="Dried arrangements.",
            category=Plant.Category.HERBS, image="plants/lavender.webp", is_edible=False,
        )
        self.cosmos = Plant.objects.create(
            name="Cosmos", about="Fine foliage and pink flowers.", used_for="Cut flowers.",
            category=Plant.Category.FLOWERS, image="plants/cosmos.webp", is_edible=False,
        )

    def test_home_and_combined_catalog_filters(self):
        response = self.client.get(reverse("main:home"))
        self.assertContains(response, "Featured plants")
        self.assertEqual(len(response.context["featured"]), 3)
        url = reverse("plants:catalog")
        self.assertEqual(len(self.client.get(url).context["plants"]), 4)
        response = self.client.get(url, {"category": "herbs", "is_edible": "yes"})
        self.assertEqual(response.context["plants"], [self.rosemary, self.basil])
        self.assertContains(response, 'value="yes" selected')
        self.assertContains(response, 'value="herbs" selected')
        response = self.client.get(url, {"category": "herbs", "is_edible": "no"})
        self.assertEqual(response.context["plants"], [self.lavender])
        response = self.client.get(url, {"category": "flowers", "is_edible": "yes"})
        self.assertContains(response, "No plants match these filters")

    def test_catalog_search_combines_with_both_filters(self):
        filters = {"q": "fragrant", "category": "herbs", "is_edible": "yes"}
        url = reverse("plants:catalog")
        response = self.client.get(url, filters)
        self.assertEqual(response.context["plants"], [self.basil])
        self.assertContains(response, 'value="fragrant"')
        response = self.client.get(url, {**filters, "category": "flowers"})
        self.assertContains(response, "No plants match these filters")

    def test_search_matches_name_description_and_use(self):
        url = reverse("plants:search")
        for query in (" BASIL ", "FRAGRANT ANNUAL", "pesto"):
            with self.subTest(query=query):
                self.assertEqual(self.client.get(url, {"q": query}).context["plants"], [self.basil])
        self.assertContains(self.client.get(url, {"q": "unlisted"}), "No matching plants")
        self.assertContains(self.client.get(url), "Find a plant")

    def test_related_plants_and_comments(self):
        url = self.basil.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(list(response.context["related"]), [self.lavender, self.rosemary])
        self.assertContains(self.client.post(url, {"full_name": "Visitor"}), "This field is required.")
        self.assertFalse(self.basil.comments.exists())
        response = self.client.post(url, {"full_name": "Visitor", "content": "Grows well on my windowsill."})
        self.assertRedirects(response, url + "#comments")
        self.assertEqual(self.basil.comments.get().full_name, "Visitor")
        self.assertContains(self.client.get(url), "Grows well on my windowsill.")

    def test_create_upload_update_delete_and_cascade(self):
        create = reverse("plants:create")
        self.assertContains(self.client.get(create), 'enctype="multipart/form-data"')
        data = {"name": "Sage", "about": "An aromatic shrub", "used_for": "Seasoning",
                "category": Plant.Category.HERBS, "is_edible": "on"}
        result = self.client.post(create, {**data, "image": SimpleUploadedFile("fake.png", b"text")})
        self.assertContains(result, "Upload a valid image")
        image = BytesIO()
        Image.new("RGB", (12, 12), "green").save(image, "PNG")
        result = self.client.post(create, {**data, "image": SimpleUploadedFile(
            "sage.png", image.getvalue(), content_type="image/png")})
        plant = Plant.objects.get(name="Sage")
        self.assertRedirects(result, plant.get_absolute_url())
        self.assertTrue(Path(plant.image.path).is_file())
        self.assertTrue(plant.image.name.startswith("img/"))
        unchanged_image = plant.image.name

        update = reverse("plants:update", args=[plant.pk])
        self.assertContains(self.client.get(update), "Edit plant")
        result = self.client.post(update, {**data, "name": "Garden sage"})
        plant.refresh_from_db()
        self.assertRedirects(result, plant.get_absolute_url())
        self.assertEqual(plant.name, "Garden sage")
        self.assertEqual(plant.image.name, unchanged_image)

        Comment.objects.create(plant=plant, full_name="Visitor", content="Beautiful.")
        delete = reverse("plants:delete", args=[plant.pk])
        self.assertContains(self.client.get(delete), "Delete Garden sage?")
        self.assertTrue(Plant.objects.filter(pk=plant.pk).exists())
        self.assertRedirects(self.client.post(delete), reverse("plants:catalog"))
        self.assertFalse(Plant.objects.filter(pk=plant.pk).exists())
        self.assertFalse(Comment.objects.filter(plant_id=plant.pk).exists())
        self.assertEqual(self.client.get(plant.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(update).status_code, 404)
        self.assertEqual(self.client.post(delete).status_code, 404)

    def test_seed_photo_edit_and_attachment_routing(self):
        call_command("seed_plants", stdout=StringIO())
        plant = Plant.objects.exclude(static_image="").first()
        url = reverse("plants:update", args=[plant.pk])
        data = {"name": plant.name, "category": plant.category,
                "about": plant.about, "used_for": plant.used_for}
        for filename, directory in [("notes.PDF", "pdf"), ("notes.txt", "fiels")]:
            response = self.client.post(url, {**data, "attachment": SimpleUploadedFile(filename, b"notes")})
            self.assertRedirects(response, plant.get_absolute_url())
            plant.refresh_from_db()
            self.assertTrue(plant.attachment.name.startswith(directory + "/"))
            self.assertTrue(Path(plant.attachment.path).is_file())
            self.assertContains(self.client.get(plant.get_absolute_url()), plant.image_url)

    def test_delete_requires_csrf(self):
        url = reverse("plants:delete", args=[self.basil.pk])
        self.assertEqual(Client(enforce_csrf_checks=True).post(url).status_code, 403)
        self.assertTrue(Plant.objects.filter(pk=self.basil.pk).exists())


class SeedTests(TestCase):
    def test_seed_uses_static_photographs_and_is_idempotent(self):
        media = self.enterContext(TemporaryDirectory())
        self.enterContext(self.settings(MEDIA_ROOT=media))
        call_command("seed_plants", stdout=StringIO())
        plants = list(Plant.objects.all())
        self.assertGreaterEqual(len(plants), 15)
        for plant in plants:
            with Image.open(finders.find(plant.static_image)) as photo:
                self.assertEqual(photo.format, "WEBP")
                photo.verify()
        first = plants[0]
        first.name = "Renamed specimen"
        first.save(update_fields=["name"])
        self.assertFalse(any(Path(media).iterdir()))
        call_command("seed_plants", stdout=StringIO())
        self.assertEqual(Plant.objects.count(), len(plants))
        self.assertTrue(Path(finders.find(first.static_image)).is_file())
