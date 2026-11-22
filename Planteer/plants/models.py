from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Plant(models.Model):
    """A plant entry that visitors can maintain from the website."""

    class Category(models.TextChoices):
        TREE = "tree", "Tree"
        FRUIT = "fruit", "Fruit"
        VEGETABLE = "vegetable", "Vegetable"
        FLOWER = "flower", "Flower"
        SUCCULENT = "succulent", "Succulent"
        HERB = "herb", "Herb"
        HOUSEPLANT = "houseplant", "Houseplant"

    name = models.CharField(max_length=120)
    about = models.TextField()
    used_for = models.TextField(blank=True)
    image = models.ImageField(upload_to="plants/", blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        return self.comments.aggregate(value=models.Avg("rating"))["value"]


class Comment(models.Model):
    """A visitor's comment and one-to-five-star rating for a plant."""

    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name="comments"
    )
    full_name = models.CharField(max_length=120)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} on {self.plant.name}"
