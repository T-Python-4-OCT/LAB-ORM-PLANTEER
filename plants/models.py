from django.db import models


class Plant(models.Model):
    """A plant in the Planteer database (fields follow the UML diagram)."""

    class Category(models.TextChoices):
        TREE = "tree", "Tree"
        FRUIT = "fruit", "Fruit"
        VEGETABLE = "vegetable", "Vegetable"
        HERB = "herb", "Herb"
        FLOWER = "flower", "Flower"
        SUCCULENT = "succulent", "Succulent"

    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.TREE)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # newest plants first

    def __str__(self):
        return self.name


class Comment(models.Model):
    """A visitor's comment on one plant."""

    # CASCADE: when a plant is deleted, its comments are deleted too.
    # related_name="comments" lets us write plant.comments.all()
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    full_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # newest comments first

    def __str__(self):
        return f"{self.full_name} on {self.plant.name}"
