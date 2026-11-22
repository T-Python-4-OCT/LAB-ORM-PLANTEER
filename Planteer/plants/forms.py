from django import forms

from .models import Comment, Plant


class PlantForm(forms.ModelForm):
    """Used by both the Add and the Update plant pages."""

    class Meta:
        model = Plant
        fields = ["name", "category", "is_edible", "about", "used_for", "image"]
        labels = {
            "name": "Plant name",
            "about": "About the plant",
            "used_for": "Used for",
            "is_edible": "This plant is edible",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "e.g. Hibiscus"}),
            "category": forms.Select(attrs={"class": "input"}),
            "is_edible": forms.CheckboxInput(attrs={"class": "switch__input"}),
            "about": forms.Textarea(attrs={"class": "input", "rows": 5,
                                           "placeholder": "Where it grows, what it looks like, how to care for it…"}),
            "used_for": forms.Textarea(attrs={"class": "input", "rows": 3,
                                              "placeholder": "Food, medicine, decoration, shade…"}),
            "image": forms.ClearableFileInput(attrs={"class": "upload__input", "accept": "image/*"}),
        }
        error_messages = {
            "name": {"required": "Give the plant a name."},
            "about": {"required": "Write a few words about the plant."},
            "used_for": {"required": "Tell us what the plant is used for."},
        }


class CommentForm(forms.ModelForm):
    """The comment form on the plant detail page. `plant` is not a field here:
    the view links the comment to its plant (comment.plant = plant)."""

    class Meta:
        model = Comment
        fields = ["full_name", "content"]
        labels = {"full_name": "Full name", "content": "Your comment"}
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "input", "placeholder": "e.g. Sara Ahmed"}),
            "content": forms.Textarea(attrs={"class": "input", "rows": 3,
                                             "placeholder": "Share a tip, a question or your experience with this plant…"}),
        }
        error_messages = {
            "full_name": {"required": "Write your name."},
            "content": {"required": "Write your comment."},
        }
