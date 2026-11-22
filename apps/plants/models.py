
from django.db import models
from django.conf import settings


class Plant(models.Model):

    class Category(models.TextChoices):
        TREE = "TREE", "Tree"
        FRUIT = "FRUIT", "Fruit"
        VEGETABLE = "VEGETABLE", "Vegetable"
        FLOWER = "FLOWER", "Flower"
        HERB = "HERB", "Herb"
        SUCCULENT = "SUCCULENT", "Succulent"

    name = models.CharField(max_length=200)

    about = models.TextField()

    used_for = models.TextField()

    image = models.ImageField(upload_to="plants/covers/")
    managed_cover_path = models.CharField(max_length=100, blank=True, editable=False)

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )

    is_edible = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plants",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")
        if self.image and not self.image._committed and (
            update_fields is None or "image" in update_fields
        ):
            self.managed_cover_path = ""
            if update_fields is not None:
                kwargs["update_fields"] = {*update_fields, "managed_cover_path"}
        super().save(*args, **kwargs)


class Comment(models.Model):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="plant_comments"
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.plant.name}"


class PlantImage(models.Model):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="plants/gallery/"
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True
    )

    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return f"{self.plant.name} - Image {self.pk}"


class PhotoImportProgress(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    fingerprint = models.CharField(max_length=64)
    completed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now=True)
    credits = models.JSONField(default=list)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["plant", "fingerprint"], name="unique_plant_photo_selection"
            )
        ]
