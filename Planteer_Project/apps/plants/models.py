from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models


class Plant(models.Model):

    class Category(models.TextChoices):
        TREES = "trees", "Trees"
        FRUITS = "fruits", "Fruits"
        VEGETABLES = "vegetables", "Vegetables"
        HERBS = "herbs", "Herbs"
        FLOWERS = "flowers", "Flowers"
        SUCCULENTS = "succulents", "Succulents"

    name = models.CharField(max_length=150)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )
    native_to = models.CharField(max_length=200)
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
        max_length=100,
        validators=[MinLengthValidator(2)]
    )

    content = models.TextField(
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(1000)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.full_name} - {self.plant.name}"