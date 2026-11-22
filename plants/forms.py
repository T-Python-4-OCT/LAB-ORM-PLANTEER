from django import forms
from .models import Comment, Plant

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "scientific_name", "about", "native_to", "used_for", "image", "category", "is_edible"]
        widgets = {
            "about": forms.Textarea(attrs={"rows": 4}),
            "used_for": forms.Textarea(attrs={"rows": 3}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]
        labels = {"full_name": "Your name", "content": "Your comment"}
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Enter your name", "autocomplete": "name"}),
            "content": forms.Textarea(attrs={"placeholder": "Write a helpful note about this plant…", "rows": 4}),
        }
