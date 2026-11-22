from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "first_name",
            "last_name",
            "email",
            "message",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Enter your first name"
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Enter your last name"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Enter your email"
            }),
            "message": forms.Textarea(attrs={
                "rows": 5,
                "placeholder": "Write your message here"
            }),
        }