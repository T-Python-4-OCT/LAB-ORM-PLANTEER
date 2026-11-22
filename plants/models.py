from django.db import models
from django.urls import reverse
from django.conf import settings
from urllib.parse import urlparse

class Plant(models.Model):
    class Category(models.TextChoices):
        INDOOR = 'indoor', 'Indoor plants'
        SUCCULENT = 'succulent', 'Succulents'
        HERB = 'herb', 'Herbs & edibles'
        FLOWERING = 'flowering', 'Flowering plants'
        VEGETABLE = 'vegetable', 'Vegetables'

    name = models.CharField(max_length=150)
    scientific_name = models.CharField(max_length=150, blank=True)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to='plants/', blank=True)
    image_url = models.URLField(blank=True, max_length=1000)
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    light = models.CharField(max_length=100, default='Bright, indirect light')
    water = models.CharField(max_length=100, default='When the topsoil feels dry')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    @property
    def photo(self):
        if self.image:
            return self.image.url
        photo_id = urlparse(self.image_url).path.rsplit('/', 1)[-1]
        if photo_id.startswith('pexels-photo-'):
            photo_id = photo_id.rsplit('.', 1)[0]
        if photo_id.startswith(('photo-', 'pexels-photo-')) and (settings.BASE_DIR / 'static' / 'images' / f'{photo_id}.jpg').exists():
            return f'/static/images/{photo_id}.jpg'
        return self.image_url or '/static/images/plant-placeholder.svg'

    def get_absolute_url(self):
        return reverse('plant_detail', args=[self.pk])

    def __str__(self):
        return self.name

class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='comments')
    full_name = models.CharField(max_length=120)
    content = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
