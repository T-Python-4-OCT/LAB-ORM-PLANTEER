from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment, Plant

ARABIC_INPUT = {"lang": "ar", "dir": "rtl"}


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            "name",
            "name_ar",
            "category",
            "about",
            "about_ar",
            "used_for",
            "used_for_ar",
            "image",
            "is_edible",
        ]
        labels = {
            "name": _("Name"),
            "name_ar": _("Name in Arabic"),
            "category": _("Category"),
            "about": _("About"),
            "about_ar": _("About, in Arabic"),
            "used_for": _("Used for"),
            "used_for_ar": _("Used for, in Arabic"),
            "image": _("Image"),
            "is_edible": _("Edible"),
        }
        help_texts = {
            field: _("Optional. Shown when the site is in Arabic.")
            for field in ("name_ar", "about_ar", "used_for_ar")
        }
        widgets = {
            "name": forms.TextInput(attrs={"dir": "auto"}),
            "name_ar": forms.TextInput(attrs=ARABIC_INPUT),
            "about": forms.Textarea(attrs={"rows": 4, "dir": "auto"}),
            "about_ar": forms.Textarea(attrs={"rows": 4, **ARABIC_INPUT}),
            "used_for": forms.Textarea(attrs={"rows": 3, "dir": "auto"}),
            "used_for_ar": forms.Textarea(attrs={"rows": 3, **ARABIC_INPUT}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["full_name", "content"]
        labels = {"full_name": _("Full name"), "content": _("Comment")}
        widgets = {
            "full_name": forms.TextInput(attrs={"dir": "auto"}),
            "content": forms.Textarea(attrs={"rows": 4, "dir": "auto"}),
        }


class PlantFilterForm(forms.Form):
    category = forms.ChoiceField(
        label=_("Category"),
        choices=[("", _("All categories")), *Plant.Category.choices],
        required=False,
    )
    is_edible = forms.TypedChoiceField(
        label=_("Edibility"),
        choices=[("", _("Any")), ("true", _("Edible")), ("false", _("Not edible"))],
        coerce=lambda value: value == "true",
        empty_value=None,
        required=False,
    )
