from django.test import TestCase
from django.urls import reverse

from .models import Contact


class MainViewsTests(TestCase):
    def test_home(self):
        self.assertEqual(self.client.get(reverse('main:home')).status_code, 200)

    def test_contact_message_saved_and_listed(self):
        res = self.client.post(reverse('main:contact'), {
            'first_name': 'Ahmed', 'last_name': 'Mohammed',
            'email': 'ahmed@example.com', 'message': 'Hello'})
        self.assertRedirects(res, reverse('main:contact'))
        self.assertEqual(Contact.objects.count(), 1)
        self.assertContains(self.client.get(reverse('main:contact_messages')), 'ahmed@example.com')

    def test_contact_invalid_email(self):
        self.client.post(reverse('main:contact'), {
            'first_name': 'A', 'last_name': 'B', 'email': 'bad', 'message': 'x'})
        self.assertFalse(Contact.objects.exists())
