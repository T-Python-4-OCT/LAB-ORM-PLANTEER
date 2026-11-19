from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = [  # noqa: RUF012
            "full_name",
            "content",
        ]

        labels = {  # noqa: RUF012
            "full_name": "Full Name",
            "content": "Your Comment",
        }

        widgets = {  # noqa: RUF012
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
                "minlength": 2,
                "maxlength": 100,
                "data-trim": "",
            }),

            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Write your comment...",
                "rows": 4,
                "minlength": 3,
                "maxlength": 1000,
                "data-trim": "",
            }),
        }