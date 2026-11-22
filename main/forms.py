from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "message"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Jane"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Smitherton"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@janesfakedomain.net"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Enter your question or message"}),
        }
