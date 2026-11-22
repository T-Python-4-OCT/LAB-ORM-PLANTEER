from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'Your first name'}), 'last_name': forms.TextInput(attrs={'placeholder': 'Your last name'}), 'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}), 'message': forms.Textarea(attrs={'placeholder': 'Let’s talk plants…', 'rows': 5})}
