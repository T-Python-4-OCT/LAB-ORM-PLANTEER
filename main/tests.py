from datetime import datetime, timezone
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Contact


class ContactTests(TestCase):
    def test_contact_time_and_staff_inbox(self):
        created_at = datetime(2026, 1, 1, 22, 15, tzinfo=timezone.utc)
        with patch("django.utils.timezone.now", return_value=created_at):
            response = self.client.post(
                "/contact/",
                {
                    "first_name": "Noura",
                    "last_name": "Ali",
                    "email": "noura@example.com",
                    "message": "A message about the catalog.",
                },
            )
        self.assertRedirects(response, "/contact/")
        self.assertEqual(Contact.objects.get().created_at, created_at)
        self.assertRedirects(
            self.client.get("/contact/messages/"),
            "/admin/login/?next=/contact/messages/",
        )

        staff = get_user_model().objects.create_user(username="staff", is_staff=True)
        self.client.force_login(staff)
        inbox = self.client.get("/contact/messages/")
        self.assertContains(inbox, "A message about the catalog.")
        self.assertContains(inbox, "2 Jan 2026, 01:15 Riyadh time")


class LanguageTests(TestCase):
    def test_switching_between_arabic_and_english(self):
        response = self.client.post("/i18n/setlang/", {"language": "ar", "next": "/plants/all/"})
        self.assertRedirects(response, "/plants/all/")

        trees = self.client.get("/plants/all/", {"category": "tree"})
        self.assertContains(trees, '<html lang="ar" dir="rtl">')
        self.assertContains(trees, "كل النباتات")
        self.assertContains(trees, "5 نباتات")
        self.assertContains(trees, "السدر")

        self.client.post("/i18n/setlang/", {"language": "en", "next": "/"})
        home = self.client.get("/")
        self.assertContains(home, '<html lang="en" dir="ltr">')
        self.assertContains(home, "Get to know your plants.")
