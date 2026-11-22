from django import forms

from .models import Comment, Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about', 'used_for', 'image', 'category', 'is_edible']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
            'used_for': forms.Textarea(attrs={'rows': 3}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'content']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }
