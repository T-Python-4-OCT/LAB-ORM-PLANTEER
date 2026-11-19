
from django.db import models


class Plant(models.Model):

    CATEGORY_CHOICES = [
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
        ('Succulent', 'Succulent'),
        ('Herb', 'Herb'),
        ('Flowering', 'Flowering'),
        ('Tree', 'Tree'),
    ]

    name = models.CharField(max_length=100)

    scientific_name = models.CharField(max_length=150)

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    is_edible = models.BooleanField(default=False)

    sunlight = models.CharField(max_length=100)

    water = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to='plants/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Comment(models.Model):

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    full_name = models.CharField(max_length=100)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} - {self.plant.name}'

