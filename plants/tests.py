from django.test import TestCase
from django.urls import reverse

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
