from django import forms
from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            "name",
            "about",
            "used_for",
            "image",
            "category",
            "is_edible",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Enter plant name"
            }),
            "about": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Describe the plant"
            }),
            "used_for": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "What is this plant used for?"
            }),
        }