from django import forms
from django.core.files.uploadedfile import UploadedFile

from apps.validators import validate_person_name

from .models import Comment, Plant


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = [  # noqa: RUF012
            "full_name",
            "content",
        ]

        labels = {  # noqa: RUF012
            "full_name": "Full Name",
            "content": "Your Comment",
        }

        widgets = {  # noqa: RUF012
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
                "minlength": 5,
                "maxlength": 25,
                "data-trim": "",
                "data-name": "",
            }),

            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write your comment...",
                "rows": 3,
                "minlength": 10,
                "maxlength": 150,
                "data-trim": "",
            }),
        }

    def clean_full_name(self):
        return validate_person_name(
            self.cleaned_data["full_name"]
        )


class PlantForm(forms.ModelForm):

    class Meta:
        model = Plant

        fields = [  # noqa: RUF012
            "name",
            "category",
            "about",
            "native_to",
            "used_for",
            "is_edible",
            "image",
        ]

        labels = {  # noqa: RUF012
            "name": "Plant Name",
            "category": "Category",
            "about": "About the Plant",
            "native_to": "Native to",
            "used_for": "Used For",
            "is_edible": "Is Edible",
            "image": "Plant Image",
        }

        widgets = {  # noqa: RUF012
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter plant name",
                "minlength": 2,
                "maxlength": 50,
                "data-trim": "",
            }),

            "category": forms.Select(attrs={
                "class": "form-select",
            }),

            "about": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Describe the plant...",
                "rows": 3,
                "minlength": 10,
                "maxlength": 200,
                "data-trim": "",
            }),

            "native_to": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Country or region",
                "minlength": 3,
                "maxlength": 50,
                "data-trim": "",
            }),

            "used_for": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Describe the plant uses...",
                "rows": 3,
                "minlength": 1,
                "maxlength": 200,
                "data-trim": "",
            }),

            "is_edible": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),

            "image": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/jpeg,image/png,image/webp",
            }),
        }

    def clean_image(self):

        image = self.cleaned_data.get("image")

        if isinstance(image, UploadedFile):

            if image.size > 5 * 1024 * 1024:

                raise forms.ValidationError(
                    "Image size cannot exceed 5 MB."
                )

            image_format = getattr(
                getattr(image, "image", None),
                "format",
                None
            )

            if image_format not in {"JPEG", "PNG", "WEBP"}:

                raise forms.ValidationError(
                    "Only JPG, PNG and WEBP images are allowed."
                )

        return image