from datetime import datetime, timezone
from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from .models import Comment, Plant


class PlantTests(TestCase):
    def test_catalog_filters_category_and_both_edibility_choices(self):
        fruits = {"Garden strawberry", "Pomegranate", "Sweet orange"}
        vegetables = {"Broccoli", "Carrot", "Hummayd", "Romaine lettuce"}
        edible_trees = {"Doum palm", "Ghaf", "Sidr"}
        shrubs = {"Arfaj", "Fringed lavender"}
        edible = fruits | vegetables | edible_trees | {
            "Cinnamon basil", "Rosemary", "Calendula", "English lavender", "Fringed lavender",
        }
        not_edible = {
            "Moth orchid", "Snake plant", "Golden pothos", "Golden chain tree", "Samr", "Arfaj",
        }
        cases = [
            ({}, edible | not_edible),
            ({"category": "flower"}, {"Calendula", "English lavender", "Moth orchid"}),
            ({"category": "fruit", "is_edible": "true"}, fruits),
            ({"category": "vegetable", "is_edible": "true"}, vegetables),
            ({"category": "tree", "is_edible": "true"}, edible_trees),
            ({"category": "shrub"}, shrubs),
            ({"is_edible": "true"}, edible),
            ({"is_edible": "false"}, not_edible),
            ({"category": "flower", "is_edible": "false"}, {"Moth orchid"}),
            ({"category": "houseplant", "is_edible": "true"}, set()),
        ]
        for filters, names in cases:
            with self.subTest(filters=filters):
                response = self.client.get("/plants/all/", filters)
                self.assertEqual(response.status_code, 200)
                self.assertSetEqual({plant.name for plant in response.context["plants"]}, names)

    def test_search_saudi_plants_by_region_and_arabic_name(self):
        saudi_plants = self.client.get("/plants/search/", {"q": "Saudi Arabia"})
        self.assertSetEqual(
            {plant.name for plant in saudi_plants.context["plants"]},
            {"Arfaj", "Doum palm", "Fringed lavender", "Ghaf", "Hummayd", "Samr", "Sidr"},
        )
        sidr = self.client.get("/plants/search/", {"q": "السدر"})
        self.assertEqual([plant.name for plant in sidr.context["plants"]], ["Sidr"])

    def test_arabic_content_is_searchable_and_shown_in_arabic(self):
        self.client.cookies[settings.LANGUAGE_COOKIE_NAME] = "ar"
        search = self.client.get("/plants/search/", {"q": "الخزامى"})
        self.assertSetEqual(
            {plant.name for plant in search.context["plants"]},
            {"English lavender", "Fringed lavender"},
        )
        self.assertContains(search, "نتيجتان عن «الخزامى»")

        sidr = Plant.objects.get(name="Sidr")
        detail = self.client.get(f"/plants/{sidr.pk}/detail/")
        self.assertContains(detail, '<h1 dir="auto">السدر</h1>', html=True)
        self.assertContains(detail, "شجرة")
        self.assertContains(detail, "بتوقيت الرياض")

    def test_search_related_plants_and_riyadh_comment_time(self):
        search = self.client.get("/plants/search/", {"q": "  BASIL  "})
        self.assertContains(search, "Cinnamon basil")
        self.assertNotContains(search, "Moth orchid")
        basil = Plant.objects.get(name="Cinnamon basil")
        url = f"/plants/{basil.pk}/detail/"
        detail = self.client.get(url)
        self.assertEqual([plant.name for plant in detail.context["related"]], ["Rosemary"])
        created_at = datetime(2026, 1, 1, 22, 15, tzinfo=timezone.utc)

        with patch("django.utils.timezone.now", return_value=created_at):
            response = self.client.post(url, {"full_name": "Noura", "content": "Lovely plant."})
        self.assertRedirects(response, url + "#comments")
        self.assertEqual(Comment.objects.get(plant=basil).created_at, created_at)
        self.assertContains(self.client.get(url), "2 Jan 2026, 01:15 Riyadh time")

    def test_plant_image_upload_update_and_confirmed_delete(self):
        image = BytesIO()
        Image.new("RGB", (8, 8), "green").save(image, format="PNG")
        fields = {
            "name": "Spearmint",
            "category": "herb",
            "about": "A fragrant herb.",
            "used_for": "Cooking",
            "is_edible": "on",
        }

        with TemporaryDirectory() as media, self.settings(MEDIA_ROOT=media):
            upload = SimpleUploadedFile("mint.png", image.getvalue(), content_type="image/png")
            response = self.client.post("/plants/new/", {**fields, "image": upload})
            plant = Plant.objects.get(name="Spearmint")
            detail_url = f"/plants/{plant.pk}/detail/"
            self.assertRedirects(response, detail_url)
            self.assertTrue(plant.image.storage.exists(plant.image.name))
            self.assertContains(self.client.get(detail_url), "Riyadh time")

            fields["name"] = "Garden mint"
            response = self.client.post(f"/plants/{plant.pk}/update/", fields)
            self.assertRedirects(response, detail_url)
            plant.refresh_from_db()
            self.assertEqual(plant.name, "Garden mint")
            self.assertTrue(plant.image.storage.exists(plant.image.name))

            delete_url = f"/plants/{plant.pk}/delete/"
            self.assertContains(self.client.get(delete_url), "Delete Garden mint?")
            self.assertTrue(Plant.objects.filter(pk=plant.pk).exists())
            self.assertRedirects(self.client.post(delete_url), "/plants/all/")
            self.assertFalse(Plant.objects.filter(pk=plant.pk).exists())
