from django.db import models


class Plant(models.Model):
    class Category(models.TextChoices):
        TREE = "tree", "Tree"
        FRUIT = "fruit", "Fruit"
        VEGETABLE = "vegetable", "Vegetable"
        FLOWER = "flower", "Flower"
        HERB = "herb", "Herb"

    name = models.CharField(max_length=200)
    about = models.TextField()
    used_for = models.TextField()
    native_to = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="plants/images/")
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.plant.name}"