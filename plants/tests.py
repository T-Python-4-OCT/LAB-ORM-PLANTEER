import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Comment, Plant

TEMP_MEDIA = tempfile.mkdtemp()


def fake_image(name='plant.png'):
    buf = io.BytesIO()
    Image.new('RGB', (10, 10), 'green').save(buf, 'PNG')
    return SimpleUploadedFile(name, buf.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class PlantViewsTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def make_plant(self, name, category='fruit', is_edible=True):
        return Plant.objects.create(name=name, about='about', used_for='food',
                                    image=fake_image(), category=category, is_edible=is_edible)

    def test_all_plants_filters(self):
        self.make_plant('Mango', 'fruit', True)
        self.make_plant('Oak', 'tree', False)
        url = reverse('plants:all_plants')
        self.assertContains(self.client.get(url), 'Mango')
        res = self.client.get(url, {'category': 'tree'})
        self.assertContains(res, 'Oak')
        self.assertNotContains(res, 'Mango')
        res = self.client.get(url, {'is_edible': 'yes'})
        self.assertContains(res, 'Mango')
        self.assertNotContains(res, 'Oak')

    def test_detail_shows_related_same_category_only(self):
        mango = self.make_plant('Mango', 'fruit')
        self.make_plant('Pomegranate', 'fruit')
        self.make_plant('Oak', 'tree')
        res = self.client.get(reverse('plants:plant_detail', args=[mango.id]))
        self.assertEqual(list(res.context['related_plants'].values_list('name', flat=True)), ['Pomegranate'])

    def test_add_comment(self):
        plant = self.make_plant('Mango')
        url = reverse('plants:plant_detail', args=[plant.id])
        res = self.client.post(url, {'full_name': 'Ahmed', 'content': 'Love it'})
        self.assertRedirects(res, url)
        self.assertEqual(Comment.objects.get().plant, plant)

    def test_create_update_delete(self):
        res = self.client.post(reverse('plants:new_plant'), {
            'name': 'Basil', 'about': 'herb', 'used_for': 'pesto',
            'image': fake_image(), 'category': 'herb', 'is_edible': 'on'})
        plant = Plant.objects.get(name='Basil')
        self.assertRedirects(res, reverse('plants:plant_detail', args=[plant.id]))
        self.assertTrue(plant.is_edible)

        self.client.post(reverse('plants:update_plant', args=[plant.id]), {
            'name': 'Sweet Basil', 'about': 'herb', 'used_for': 'pesto', 'category': 'herb'})
        plant.refresh_from_db()
        self.assertEqual(plant.name, 'Sweet Basil')
        self.assertFalse(plant.is_edible)

        self.assertEqual(self.client.get(reverse('plants:delete_plant', args=[plant.id])).status_code, 405)
        self.client.post(reverse('plants:delete_plant', args=[plant.id]))
        self.assertFalse(Plant.objects.exists())

    def test_all_plants_paginated_by_nine_and_keeps_filters(self):
        for i in range(12):
            self.make_plant(f'Fruit {i}', 'fruit')
        self.make_plant('Oak', 'tree')
        url = reverse('plants:all_plants')

        page1 = self.client.get(url)
        self.assertEqual(len(page1.context['plants']), 9)
        page2 = self.client.get(url, {'page': 2})
        self.assertEqual(len(page2.context['plants']), 4)

        filtered = self.client.get(url, {'category': 'fruit', 'page': 2})
        self.assertEqual(len(filtered.context['plants']), 3)
        self.assertContains(filtered, '?category=fruit&page=1')

    def test_search(self):
        self.make_plant('Mango')
        self.make_plant('Oak', 'tree')
        res = self.client.get(reverse('plants:search'), {'q': 'man'})
        self.assertContains(res, 'Mango')
        self.assertNotContains(res, 'Oak')
