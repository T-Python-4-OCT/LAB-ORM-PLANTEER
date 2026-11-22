from django import forms

from .models import Comment, Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "about", "used_for", "native_to", "category", "is_edible", "image"]
        labels = {
            "used_for": "Used for",
            "native_to": "Native to",
            "is_edible": "Is edible",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Date Palm"}),
            "about": forms.Textarea(attrs={"rows": 4, "placeholder": "A brief description of the plant"}),
            "used_for": forms.Textarea(attrs={"rows": 3, "placeholder": "What is this plant used for?"}),
            "native_to": forms.TextInput(attrs={"placeholder": "e.g. Saudi Arabia, Iraq, Egypt"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]
        labels = {"full_name": "Full name", "content": "Comment"}
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Share your thoughts about this plant"}),
        }
