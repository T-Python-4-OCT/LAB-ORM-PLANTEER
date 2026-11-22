"""All the project's models live in this one file — each table is its own class:

    Plant    -> the plants (name, about, used_for, image, category, is_edible, created_at)
    Comment  -> visitors' comments on a plant   (many comments -> one plant)
    Contact  -> messages sent from the Contact Us page

Primary keys: Django adds an auto-increment `id` primary key to every class.
Relationship: Comment.plant is a ForeignKey, so each comment stores `plant_id`,
which points to the primary key (id) of one Plant. One plant -> many comments.
"""
from django.db import models


class Plant(models.Model):
    """A plant in the Planteer database."""

    class Category(models.TextChoices):
        TREE = "tree", "Tree"
        FRUIT = "fruit", "Fruit"
        VEGETABLE = "vegetable", "Vegetable"
        HERB = "herb", "Herb"
        FLOWER = "flower", "Flower"
        SUCCULENT = "succulent", "Succulent"

    name = models.CharField(max_length=128)
    about = models.TextField()
    used_for = models.TextField()
    # if a plant is created without a photo (e.g. by the seed command offline) it gets the placeholder
    image = models.ImageField(upload_to="plants/", default="plants/default.jpg")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.HERB)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return self.name


class Comment(models.Model):
    """A visitor's comment on a plant — many comments belong to one plant."""

    # ForeignKey = many-to-one. on_delete=CASCADE: deleting a plant deletes its comments.
    # related_name="comments" lets us write plant.comments.all()
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    full_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # newest comment first

    def __str__(self):
        return f"{self.full_name} on {self.plant.name}"


class Contact(models.Model):
    """A message sent from the Contact Us page."""

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # newest message first

    def __str__(self):
        return f"{self.first_name} {self.last_name} <{self.email}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
