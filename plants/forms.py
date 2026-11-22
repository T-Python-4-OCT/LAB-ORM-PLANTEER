from django import forms

from .models import Comment, Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "about", "used_for", "category", "is_edible", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Plant name"}),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Brief about the plant"}),
            "used_for": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "What is this plant used for?"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "is_edible": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Write your comment..."}),
        }
