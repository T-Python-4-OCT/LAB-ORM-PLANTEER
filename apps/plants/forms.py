
from django import forms
from .models import Plant, Comment, PlantImage


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
                "placeholder": "Plant name"
            }),
            "about": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "About this plant"
            }),
            "used_for": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "What is this plant used for?"
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Write your comment..."
            }),
        }


class PlantImageForm(forms.ModelForm):
    class Meta:
        model = PlantImage
        fields = ["image", "alt_text", "position"]
