from django import forms

from apps.validators import validate_person_name

from .models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact

        fields = [  # noqa: RUF012
            "first_name",
            "last_name",
            "email",
            "message",
        ]

        labels = {  # noqa: RUF012
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "message": "Your Message",
        }

        widgets = {  # noqa: RUF012
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First name",
                "minlength": 3,
                "maxlength": 15,
                "data-trim": "",
                "data-name": "",
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last name",
                "minlength": 3,
                "maxlength": 15,
                "data-trim": "",
                "data-name": "",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "email@example.com",
                "maxlength": 254,
                "data-trim": "",
            }),

            "message": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter your message...",
                "rows": 4,
                "minlength": 10,
                "maxlength": 150,
                "data-trim": "",
            }),
        }

    def clean_first_name(self):
        return validate_person_name(
            self.cleaned_data["first_name"]
        )

    def clean_last_name(self):
        return validate_person_name(
            self.cleaned_data["last_name"]
        )