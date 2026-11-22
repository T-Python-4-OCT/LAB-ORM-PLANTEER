from django import forms
from .models import Comment, Plant

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
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]