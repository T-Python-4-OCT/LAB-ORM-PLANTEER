from django import forms

from plants.models import Contact  # all models live in plants/models.py


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "message"]
        labels = {
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email address",
            "message": "Your message",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input", "placeholder": "Jane"}),
            "last_name": forms.TextInput(attrs={"class": "input", "placeholder": "Smitherton"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "email@janesfakedomain.net"}),
            "message": forms.Textarea(attrs={"class": "input", "rows": 5,
                                             "placeholder": "Enter your question or message"}),
        }
        error_messages = {
            "first_name": {"required": "Write your first name."},
            "last_name": {"required": "Write your last name."},
            "email": {"required": "Write your email.", "invalid": "Enter a valid email address."},
            "message": {"required": "Write your message."},
        }
