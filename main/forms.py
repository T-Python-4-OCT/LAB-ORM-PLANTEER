from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email address',
            'message': 'Your message',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Wessam'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Alomari'}),
            'email': forms.EmailInput(attrs={'placeholder': 'wessam.alomari@gmail.com'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter your question or message'}),
        }