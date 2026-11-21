from django.db import models


class Plant(models.Model):
    """A plant (fields from the task's UML)."""

    # TextChoices: the database saves the value ("tree"), the page shows the label ("Tree")
    class Category(models.TextChoices):
        TREE = "tree", "Tree"
        FRUIT = "fruit", "Fruit"
        VEGETABLES = "vegetables", "Vegetables"
        HERB = "herb", "Herb"
        FLOWER = "flower", "Flower"
        SUCCULENT = "succulent", "Succulent"

    name = models.CharField(max_length=1024)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="images/")
    category = models.CharField(max_length=64, choices=Category.choices)
    is_edible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Comment(models.Model):
    """A visitor's comment on a plant.

    ForeignKey: every comment belongs to one plant, and a plant can have many comments.
    on_delete=CASCADE: deleting a plant deletes its comments too.
    related_name="comments": plant.comments.all() gives the comments of a plant.
    """

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    full_name = models.CharField(max_length=1024)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.full_name} on {self.plant}"
