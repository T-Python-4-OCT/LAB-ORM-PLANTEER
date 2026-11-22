from django.db import models

# Create your models here
class Plant(models.Model):

    class Category(models.TextChoices):
        INDOOR = "Indoor", "Indoor"
        OUTDOOR = "Outdoor", "Outdoor"
        SUCCULENTS = "Succulents", "Succulents"
        HERBS = "Herbs", "Herbs"
        FLOWERING = "Flowering", "Flowering"
        TREES = "Trees", "Trees"

    name = models.CharField(max_length=100)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    full_name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.full_name} on {self.plant.name}"
