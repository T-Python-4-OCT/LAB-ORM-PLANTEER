from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            "name",
            "about",
            "used_for",
            "image",
            "image_url",
            "category",
            "is_edible",
        ]
        widgets = {
            "about": forms.Textarea(attrs={"rows": 4}),
            "used_for": forms.Textarea(attrs={"rows": 3}),
            "image_url": forms.URLInput(
                attrs={"placeholder": "https://example.com/plant.jpg"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("image") and not cleaned_data.get("image_url"):
            if not (self.instance and (self.instance.image or self.instance.image_url)):
                raise ValidationError("Upload an image or provide an image URL.")
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "rating", "content"]
        widgets = {
            "rating": forms.Select(
                choices=[(value, f"{value} star{'s' if value != 1 else ''}") for value in range(5, 0, -1)]
            ),
            "content": forms.Textarea(attrs={"rows": 3}),
        }
