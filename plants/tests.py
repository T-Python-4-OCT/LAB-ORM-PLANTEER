from django.test import TestCase
from django.urls import reverse

from main.models import Contact

from .models import Comment, Plant


class PlanteerTests(TestCase):
    fixtures = ["plants"]

    def test_pages_load(self):
        urls = [
            reverse("main:home_view"),
            reverse("plants:all_plants_view"),
            reverse("plants:plant_detail_view", args=[1]),
            reverse("plants:add_plant_view"),
            reverse("plants:update_plant_view", args=[1]),
            reverse("plants:search_plants_view") + "?search=palm",
            reverse("main:contact_view"),
            reverse("main:contact_messages_view"),
        ]
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_filter_category_and_edible(self):
        res = self.client.get(reverse("plants:all_plants_view"), {"category": "succulent", "is_edible": "yes"})
        self.assertEqual([p.name for p in res.context["plants"]], ["Prickly Pear"])

    def test_related_plants_same_category(self):
        res = self.client.get(reverse("plants:plant_detail_view", args=[1]))
        related = list(res.context["related_plants"])
        self.assertTrue(related)
        self.assertTrue(all(p.category == "tree" and p.pk != 1 for p in related))

    def test_add_comment(self):
        self.client.post(reverse("plants:plant_detail_view", args=[2]), {"full_name": "Ali", "content": "Nice"})
        self.assertTrue(Comment.objects.filter(plant_id=2, full_name="Ali").exists())

    def test_search(self):
        res = self.client.get(reverse("plants:search_plants_view"), {"search": "mint"})
        self.assertIn("Mint", [p.name for p in res.context["plants"]])

    def test_update_and_delete(self):
        self.client.post(reverse("plants:update_plant_view", args=[3]), {
            "name": "Neem Tree", "about": "a", "used_for": "b", "native_to": "", "category": "tree",
        })
        self.assertEqual(Plant.objects.get(pk=3).name, "Neem Tree")
        self.client.post(reverse("plants:delete_plant_view", args=[3]))
        self.assertFalse(Plant.objects.filter(pk=3).exists())

    def test_contact(self):
        self.client.post(reverse("main:contact_view"), {
            "first_name": "Ahmed", "last_name": "Mohammed", "email": "a@example.com", "message": "Hi",
        })
        self.assertEqual(Contact.objects.count(), 1)
