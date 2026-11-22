from django.db import models

# Create your models here.
class Plant(models.Model):

    class Category(models.TextChoices):
        INDOOR = "Indoor", "Indoor" # Indoor Plants
        OUTDOOR = "Outdoor", "Outdoor" # Outdoor Plants
        SUCCULENTS = "Succulents", "Succulents" # Succulents Plants
        HERBS = "Herbs", "Herbs" # Herps Plants
        FLOWERING = "Flowering", "Flowering" # Flowering Plants
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
