from django.test import TestCase
from django.urls import reverse

from plants.models import Plant

from .models import Contact


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


class ContactTests(TestCase):
    def valid_data(self, **changes):
        data = {
            "first_name": "Ahmed",
            "last_name": "Mohammed",
            "email": "ahmed@example.com",
            "message": "Please add the Sidr tree to Planteer.",
        }
        data.update(changes)
        return data

    def test_contact_page_loads(self):
        response = self.client.get(reverse("main:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact us")

    def test_valid_message_is_saved(self):
        response = self.client.post(reverse("main:contact"), self.valid_data(), follow=True)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertRedirects(response, reverse("main:contact"))
        self.assertContains(response, "We received your message")

    def test_invalid_email_is_rejected(self):
        response = self.client.post(reverse("main:contact"), self.valid_data(email="not-an-email"))
        self.assertEqual(Contact.objects.count(), 0)
        self.assertIn("email", response.context["form"].errors)

    def test_empty_form_is_rejected(self):
        self.client.post(reverse("main:contact"), {})
        self.assertEqual(Contact.objects.count(), 0)

    def test_too_short_message_is_rejected(self):
        self.client.post(reverse("main:contact"), self.valid_data(message="Hi"))
        self.assertEqual(Contact.objects.count(), 0)

    def test_messages_page_lists_messages_newest_first(self):
        old = Contact.objects.create(first_name="A", last_name="One", email="a@example.com", message="First message")
        new = Contact.objects.create(first_name="B", last_name="Two", email="b@example.com", message="Second message")
        response = self.client.get(reverse("main:contact_messages"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["contact_messages"]), [new, old])
        self.assertContains(response, "b@example.com")

    def test_messages_page_empty_state(self):
        response = self.client.get(reverse("main:contact_messages"))
        self.assertContains(response, "No messages yet")
