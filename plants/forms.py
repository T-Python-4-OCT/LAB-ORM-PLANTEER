from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]
        labels = {"full_name": "Your name", "content": "Your comment"}
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Enter your name", "autocomplete": "name"}),
            "content": forms.Textarea(attrs={"placeholder": "Write a helpful note about this plant…", "rows": 4}),
        }
