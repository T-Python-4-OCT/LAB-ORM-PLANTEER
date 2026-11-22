from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "message"]
        labels = {"first_name": "First name", "last_name": "Last name", "email": "Email address", "message": "Your message"}
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name", "autocomplete": "given-name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name", "autocomplete": "family-name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "message": forms.Textarea(attrs={"placeholder": "Write your question or message…", "rows": 5}),
        }
