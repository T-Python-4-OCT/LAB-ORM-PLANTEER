from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
)
from django.db import models


class Contact(models.Model):

    first_name = models.CharField(
        max_length=15,
        validators=[MinLengthValidator(3)]
    )

    last_name = models.CharField(
        max_length=15,
        validators=[MinLengthValidator(3)]
    )

    email = models.EmailField()

    message = models.TextField(
        max_length=150,
        validators=[
            MinLengthValidator(10),
            MaxLengthValidator(150)
        ]
    )

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"