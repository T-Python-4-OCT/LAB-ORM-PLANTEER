from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "message"]
        labels = {"email": "Email address", "message": "Your message"}
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Jane"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Smith"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Enter your question or message"}),
        }

    def clean_message(self):
        message = self.cleaned_data["message"]
        if len(message) < 10:
            raise forms.ValidationError("Please write at least 10 characters.")
        return message
