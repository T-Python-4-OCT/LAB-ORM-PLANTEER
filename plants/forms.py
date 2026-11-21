"""ModelForms: Django builds the fields from the models, checks them, and form.save() writes to the database."""

from django import forms

from plants.models import Comment, Plant

IMAGE_MAX_MB = 5


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ["name", "about", "used_for", "image", "category", "is_edible"]
        labels = {
            "name": "Plant Name",
            "about": "About",
            "used_for": "Used For",
            "image": "Image",
            "category": "Category",
            "is_edible": "Is Edible",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Pomegranate"}),
            "about": forms.Textarea(attrs={"rows": 4, "placeholder": "Brief about the plant"}),
            "used_for": forms.Textarea(attrs={"rows": 3, "placeholder": "e.g. Salads and cooking"}),
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        # Only a new upload has content_type (on the update page, no new file = the old image)
        if image and hasattr(image, "content_type") and image.size > IMAGE_MAX_MB * 1024 * 1024:
            raise forms.ValidationError(f"The image is too big (max {IMAGE_MAX_MB} MB).")
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]     # the plant is set in the view
        labels = {"full_name": "Full Name", "content": "Comment"}
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Jane Smitherton"}),
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write your comment"}),
        }
