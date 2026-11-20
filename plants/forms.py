from django import forms
from .models import Plant, Comment


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about', 'used_for', 'image', 'category', 'is_edible']
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
            'used_for': forms.Textarea(attrs={'rows': 3}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'content']
        widgets = {'content': forms.Textarea(attrs={'rows': 3})}