from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
)
from django.db import models


class Plant(models.Model):

    class Category(models.TextChoices):
        TREES = "trees", "Trees"
        FRUITS = "fruits", "Fruits"
        VEGETABLES = "vegetables", "Vegetables"
        HERBS = "herbs", "Herbs"
        FLOWERS = "flowers", "Flowers"
        SUCCULENTS = "succulents", "Succulents"

    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2)]
    )

    about = models.TextField(
        max_length=200,
        validators=[
            MinLengthValidator(10),
            MaxLengthValidator(200)
        ]
    )

    used_for = models.TextField(
        max_length=200,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(200)
        ]
    )

    image = models.ImageField(upload_to="plants/")

    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    native_to = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(3)]
    )

    is_edible = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.name


class Comment(models.Model):

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    full_name = models.CharField(
        max_length=25,
        validators=[MinLengthValidator(5)]
    )

    content = models.TextField(
        max_length=150,
        validators=[
            MinLengthValidator(10),
            MaxLengthValidator(150)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.full_name} - {self.plant.name}"