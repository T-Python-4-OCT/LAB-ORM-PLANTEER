
from django.db import models


class Plant(models.Model):
    class Category(models.TextChoices):
        FLOWER = "flower", "Flowers"
        HERB = "herb", "Herbs"
        TREE = "tree", "Trees"
        SUCCULENT = "succulent", "Succulents"
        INDOOR = "indoor", "Indoor Plants"

    name = models.CharField(max_length=150)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    full_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.plant.name}"
