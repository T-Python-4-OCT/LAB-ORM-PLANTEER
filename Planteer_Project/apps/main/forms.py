from unicodedata import category

from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact

        fields = [# noqa: RUF012
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
                "minlength": 2,
                "maxlength": 50,
                "data-trim": "",
                "data-name": "",
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last name",
                "minlength": 2,
                "maxlength": 50,
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
                "rows": 6,
                "minlength": 10,
                "maxlength": 2000,
                "data-trim": "",
            }),
        }

    @staticmethod
    def validate_name(value):

        value = value.strip()

        valid = all(
            category(char).startswith(("L", "M"))
            or char in " -'’"
            for char in value
        )

        has_letter = any(char.isalpha() for char in value)

        if not valid or not has_letter:

            raise forms.ValidationError(
                "Please enter a valid name."
            )

        return value

    def clean_first_name(self):

        return self.validate_name(
            self.cleaned_data["first_name"]
        )

    def clean_last_name(self):

        return self.validate_name(
            self.cleaned_data["last_name"]
        )