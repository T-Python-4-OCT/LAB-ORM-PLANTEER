from django.test import TestCase
from django.urls import reverse

from plants.models import Plant


class HomePageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("main:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/home.html")
        self.assertTemplateUsed(response, "base.html")

    def test_home_shows_empty_state_without_plants(self):
        response = self.client.get(reverse("main:home"))
        self.assertContains(response, "No plants yet")

    def test_home_shows_at_most_three_plants(self):
        for i in range(5):
            Plant.objects.create(name=f"Plant {i}", about="a", used_for="b", image="plants/x.jpg")
        response = self.client.get(reverse("main:home"))
        self.assertEqual(len(response.context["plants"]), 3)
