from django.db import models


class Plant(models.Model):
    class Category(models.TextChoices):
        TREE = 'Tree', 'Tree'
        FRUIT = 'Fruit', 'Fruit'
        VEGETABLE = 'Vegetable', 'Vegetable'
        HERB = 'Herb', 'Herb'
        FLOWER = 'Flower', 'Flower'
        SUCCULENT = 'Succulent', 'Succulent'

    name = models.CharField(max_length=200)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='comments')
    full_name = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} on {self.plant.name}'
