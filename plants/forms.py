from django import forms

from .models import Comment, Plant


class PlantForm(forms.ModelForm):
    """One form used for both adding and updating a plant."""

    class Meta:
        model = Plant
        fields = ["name", "category", "is_edible", "about", "used_for", "image"]
        labels = {
            "is_edible": "This plant is edible",
            "used_for": "Used for",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Date Palm"}),
            "about": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Describe the plant: what it looks like, where it grows...",
            }),
            "used_for": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "e.g. Eaten fresh, used in cooking and medicine",
            }),
            # FileInput (not the default ClearableFileInput) so the old photo is kept unless a new one is chosen
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def clean_name(self):
        # Remove extra spaces so "  Mint " is saved as "Mint"
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Plant name must be at least 2 characters.")
        return name


class CommentForm(forms.ModelForm):
    """Visitors add a comment with only their name and the text."""

    class Meta:
        model = Comment
        # "plant" is NOT in the form: the view sets it, so visitors can't change it
        fields = ["full_name", "content"]
        labels = {"full_name": "Your name", "content": "Comment"}
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "e.g. Sara Alqahtani"}),
            "content": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Share a tip or ask a question about this plant",
            }),
        }
