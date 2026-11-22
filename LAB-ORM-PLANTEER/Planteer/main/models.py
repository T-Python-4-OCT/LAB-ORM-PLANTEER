from django.db import models
from Planteer.plants.models import Comment as PlantComment


class Contact(models.Model):

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField()

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name



class MainComment(PlantComment):
    class Meta:
        proxy = True
        verbose_name = "Comment"
        verbose_name_plural = "Comments"