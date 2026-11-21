from django.db import models

class Plant(models.Model):
    class Category(models.TextChoices):
        TREE = "tree", "Tree"
        FRUIT = "fruit", "Fruit"
        VEGETABLE = "vegetable", "Vegetable"
        HERB = "herb", "Herb"
        FLOWER = "flower", "Flower"
        SUCCULENT = "succulent", "Succulent"

    name = models.CharField(max_length=120)
    scientific_name = models.CharField(max_length=160, blank=True)
    about = models.TextField()
    native_to = models.CharField(max_length=180, blank=True)
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
