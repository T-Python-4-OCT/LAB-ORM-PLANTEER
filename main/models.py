from django.db import models


class Contact(models.Model):
    """A message sent from the Contact Us page (fields from the task's UML)."""

    first_name = models.CharField(max_length=1024)
    last_name = models.CharField(max_length=1024)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
