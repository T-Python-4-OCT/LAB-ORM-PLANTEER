
from django import forms

from .models import Plant, Comment


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
                "placeholder": "Enter plant name",
            }),
            "about": forms.Textarea(attrs={
                "placeholder": "Describe this plant...",
                "rows": 5,
            }),
            "used_for": forms.Textarea(attrs={
                "placeholder": "What is this plant used for?",
                "rows": 4,
            }),
            "image": forms.FileInput(attrs={
                "accept": "image/*",
            }),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Plant name must contain at least 2 characters."
            )

        return name


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "placeholder": "Your full name",
                "minlength": "3",
                "maxlength": "100",
                "required": True,
            }),
            "content": forms.Textarea(attrs={
                "placeholder": "Share your thoughts about this plant...",
                "rows": 4,
                "minlength": "5",
                "required": True,
            }),
        }

    def clean_full_name(self):
        full_name = self.cleaned_data["full_name"].strip()

        if len(full_name) < 3:
            raise forms.ValidationError(
                "Name must contain at least 3 characters."
            )

        return full_name

    def clean_content(self):
        content = self.cleaned_data["content"].strip()

        if len(content) < 5:
            raise forms.ValidationError(
                "Comment must contain at least 5 characters."
            )

        return content
