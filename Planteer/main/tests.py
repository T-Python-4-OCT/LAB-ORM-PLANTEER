from django.test import TestCase
from django.urls import reverse

from plants.models import Contact, Plant


class MainPagesTests(TestCase):
    def test_home_shows_newest_plants(self):
        for i in range(8):
            Plant.objects.create(name=f"Plant {i}", about="a", used_for="b")
        res = self.client.get(reverse("main:home"))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.context["plants"]), 6)
        self.assertEqual(res.context["plants"][0].name, "Plant 7")  # newest first
        self.assertContains(res, reverse("plants:search"))

    def test_contact_saves_message(self):
        res = self.client.post(reverse("main:contact"), {
            "first_name": "Ahmed", "last_name": "Mohammed", "email": "moh@gmail.com", "message": "Add more cacti!",
        })
        self.assertRedirects(res, reverse("main:contact"))
        self.assertEqual(Contact.objects.get().full_name, "Ahmed Mohammed")

    def test_contact_invalid_email(self):
        res = self.client.post(reverse("main:contact"), {
            "first_name": "A", "last_name": "B", "email": "not-an-email", "message": "hi"})
        self.assertContains(res, "Enter a valid email address.")
        self.assertEqual(Contact.objects.count(), 0)

    def test_contact_messages_page(self):
        Contact.objects.create(first_name="Ahmed", last_name="Mohammed", email="moh@gmail.com", message="Hello there")
        res = self.client.get(reverse("main:contact_messages"))
        self.assertContains(res, "Ahmed Mohammed")
        self.assertContains(res, "mailto:moh@gmail.com")
        self.assertContains(res, "Hello there")
