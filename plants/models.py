from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class Plant(models.Model):
    class Category(models.TextChoices):
        HERB = "herb", _("Herb")
        FLOWER = "flower", _("Flower")
        HOUSEPLANT = "houseplant", _("Houseplant")
        TREE = "tree", _("Tree")
        SHRUB = "shrub", _("Shrub")
        FRUIT = "fruit", _("Fruit")
        VEGETABLE = "vegetable", _("Vegetable")

    name = models.CharField(max_length=120)
    about = models.TextField()
    used_for = models.TextField()
    name_ar = models.CharField(max_length=120, blank=True)
    about_ar = models.TextField(blank=True)
    used_for_ar = models.TextField(blank=True)
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]

    def __str__(self):
        return self.name

    def _localized_text(self, field):
        original = getattr(self, field)
        if (get_language() or "").startswith("ar"):
            return getattr(self, f"{field}_ar") or original
        return original

    @property
    def local_name(self):
        return self._localized_text("name")

    @property
    def local_about(self):
        return self._localized_text("about")

    @property
    def local_used_for(self):
        return self._localized_text("used_for")


class Comment(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="comments")
    full_name = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]

    def __str__(self):
        return f"{self.full_name} on {self.plant}"
