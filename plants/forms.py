from django import forms

from .models import Comment, Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "category", "about", "used_for", "image", "attachment", "is_edible", "edible_part"]
        widgets = {
            "about": forms.Textarea(attrs={"rows": 4}),
            "used_for": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {
            "image": "Upload a photograph up to 8 MB.",
            "attachment": "Optional PDF, TXT, CSV, DOCX or XLSX file.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = not self.instance.static_image

    def clean_image(self):
        image = self.cleaned_data["image"]
        if image and "image" in self.changed_data and image.size > 8 * 1024 * 1024:
            raise forms.ValidationError("Choose an image smaller than 8 MB.")
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]
        labels = {"content": "Comment"}
        widgets = {"content": forms.Textarea(attrs={"rows": 4})}
