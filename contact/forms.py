
from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "message"]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Enter your first name",
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Enter your last name",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Enter your email address",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Write your message here...",
                "rows": 6,
            }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()

        if len(first_name) < 2:
            raise forms.ValidationError(
                "First name must contain at least 2 characters."
            )

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].strip()

        if len(last_name) < 2:
            raise forms.ValidationError(
                "Last name must contain at least 2 characters."
            )

        return last_name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()

        if len(message) < 10:
            raise forms.ValidationError(
                "Message must contain at least 10 characters."
            )

        return message
