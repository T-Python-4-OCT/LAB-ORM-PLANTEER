from django.test import TestCase
from django.urls import reverse
from .models import Plant, Comment
from main.models import Contact

class PlantFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.plant = Plant.objects.create(name='Sweet basil', about='A fragrant herb', used_for='Pesto', category='herb', is_edible=True)
        cls.related = Plant.objects.create(name='Rosemary', about='An aromatic herb', used_for='Cooking', category='herb', is_edible=True)
        Plant.objects.create(name='Monstera', about='Split leaves', used_for='Decor', category='indoor')

    def test_pages_render(self):
        for url in ['/', '/plants/all/', '/plants/search/', '/plants/new/', '/contact/', '/contact/messages/', self.plant.get_absolute_url(), reverse('plant_update', args=[self.plant.pk]), reverse('plant_delete', args=[self.plant.pk])]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_search_and_combined_filters(self):
        response = self.client.get('/plants/search/', {'q': 'basil', 'category': 'herb', 'is_edible': 'true'})
        self.assertQuerySetEqual(response.context['plants'], [self.plant])
        response = self.client.get('/plants/all/', {'is_edible': 'false'})
        self.assertEqual(response.context['plants'].count(), 1)

    def test_detail_related_and_comments(self):
        response = self.client.get(self.plant.get_absolute_url())
        self.assertQuerySetEqual(response.context['related'], [self.related])
        self.client.post(self.plant.get_absolute_url(), {'full_name': 'A gardener', 'content': 'Pinch the tips!'})
        self.assertEqual(Comment.objects.get().plant, self.plant)
        self.assertEqual(self.client.post(self.plant.get_absolute_url(), {'full_name': '', 'content': ''}).status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_update_and_post_only_delete(self):
        data = {'name': 'Mint', 'about': 'Fresh herb', 'used_for': 'Tea', 'category': 'herb', 'is_edible': 'on', 'light': 'Sun', 'water': 'Regularly'}
        response = self.client.post('/plants/new/', data)
        mint = Plant.objects.get(name='Mint')
        self.assertRedirects(response, mint.get_absolute_url())
        data['name'] = 'Garden mint'
        self.client.post(reverse('plant_update', args=[mint.pk]), data)
        mint.refresh_from_db()
        self.assertEqual(mint.name, 'Garden mint')
        url = reverse('plant_delete', args=[mint.pk])
        self.client.get(url)
        self.assertTrue(Plant.objects.filter(pk=mint.pk).exists())
        self.client.post(url)
        self.assertFalse(Plant.objects.filter(pk=mint.pk).exists())

    def test_contact_validation_and_email_privacy(self):
        data = {'first_name': 'Sara', 'last_name': 'Green', 'email': 'sara@example.com', 'message': 'Hello gardeners'}
        self.assertRedirects(self.client.post('/contact/', data), '/contact/')
        self.assertEqual(Contact.objects.count(), 1)
        response = self.client.get('/contact/messages/')
        self.assertContains(response, 'Hello gardeners')
        self.assertNotContains(response, 'sara@example.com')
        data['email'] = 'invalid'
        self.assertEqual(self.client.post('/contact/', data).status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)

    def test_csrf_is_enforced(self):
        from django.test import Client
        self.assertEqual(Client(enforce_csrf_checks=True).post('/plants/new/', {}).status_code, 403)

    def test_missing_plant(self):
        self.assertEqual(self.client.get('/plants/99999/detail/').status_code, 404)
