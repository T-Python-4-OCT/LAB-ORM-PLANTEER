import re
from pathlib import Path

from django.templatetags.static import static

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse


def attachment_path(instance, filename):
    directory = "pdf" if Path(filename).suffix.lower() == ".pdf" else "fiels"
    return f"{directory}/{Path(filename).name}"


class Plant(models.Model):
    class Category(models.TextChoices):
        HOUSEPLANTS = "houseplants", "Houseplants"
        HERBS = "herbs", "Herbs"
        FLOWERS = "flowers", "Flowers"
        SUCCULENTS = "succulents", "Succulents"
        FRUIT_TREES = "fruit-trees", "Fruit trees"

    name = models.CharField(max_length=120)
    about = models.TextField(validators=[MaxLengthValidator(3000)])
    used_for = models.TextField(validators=[MaxLengthValidator(2000)])
    image = models.ImageField(upload_to="img/", blank=True)
    static_image = models.CharField(max_length=150, blank=True, editable=False)
    attachment = models.FileField(
        upload_to=attachment_path, blank=True,
        validators=[FileExtensionValidator(["pdf", "txt", "csv", "docx", "xlsx"])],
    )
    category = models.CharField(max_length=24, choices=Category.choices, db_index=True)
    is_edible = models.BooleanField(default=False)
    edible_part = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", "pk"]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.edible_part and not self.is_edible:
            raise ValidationError({"edible_part": "Select edible before specifying a part."})

    @property
    def image_url(self):
        return self.image.url if self.image else static(self.static_image)

    @property
    def card_summary(self):
        """Use a complete opening sentence when it fits the card."""
        sentence = re.split(r"(?<=[.!?])(?:\s+|$)", self.about.strip(), maxsplit=1)[0]
        if sentence and len(sentence) <= 180:
            return sentence
        return f"Explore the uses and characteristics of {self.name}."

    def get_absolute_url(self):
        return reverse("plants:detail", kwargs={"plant_id": self.pk})


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    full_name = models.CharField(max_length=100)
    content = models.TextField(validators=[MaxLengthValidator(1500)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]

    def __str__(self):
        return f"{self.full_name} on {self.plant}"
