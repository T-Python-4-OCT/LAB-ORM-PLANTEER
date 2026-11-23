from django import forms

from .models import Plant


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
            "about": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe the plant: what it looks like, where it grows..."}),
            "used_for": forms.Textarea(attrs={"rows": 3, "placeholder": "e.g. Eaten fresh, used in cooking and medicine"}),
            # FileInput (not the default ClearableFileInput) so the old photo is kept unless a new one is chosen
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def clean_name(self):
        # Remove extra spaces so "  Mint " is saved as "Mint"
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Plant name must be at least 2 characters.")
        return name
