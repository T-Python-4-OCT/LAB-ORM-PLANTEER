from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "message"]
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
            "email": _("Email"),
            "message": _("Message"),
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"dir": "auto"}),
            "last_name": forms.TextInput(attrs={"dir": "auto"}),
            "message": forms.Textarea(attrs={"rows": 5, "dir": "auto"}),
        }
