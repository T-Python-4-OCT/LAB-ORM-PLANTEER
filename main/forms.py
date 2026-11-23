from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Jane'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Smitherton'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter your question or message'}),
        }
