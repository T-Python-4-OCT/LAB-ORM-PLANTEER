from django.test import TestCase
from django.urls import reverse

from .models import Contact


class ContactTests(TestCase):
    def test_contact_submission_validation_and_persistence(self):
        url = reverse("main:contact")
        self.assertContains(self.client.get(url), "Contact us")
        data = {"first_name": "Dana", "last_name": "Ali", "email": "invalid", "message": "A suggestion."}
        invalid = self.client.post(url, data)
        self.assertContains(invalid, "Enter a valid email address.")
        self.assertFalse(Contact.objects.exists())
        response = self.client.post(url, {**data, "email": "dana@example.com"}, follow=True)
        self.assertRedirects(response, url)
        self.assertContains(response, "Your message was received.")
        self.assertEqual(Contact.objects.get().email, "dana@example.com")

    def test_visitors_can_read_messages_without_seeing_email(self):
        Contact.objects.create(first_name="Dana", last_name="Ali", email="dana@example.com",
                               message="<script>alert(1)</script>")
        url = reverse("main:inbox")
        response = self.client.get(url)
        self.assertContains(response, "Dana Ali")
        self.assertNotContains(response, "dana@example.com")
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
