from unicodedata import category

from django.core.exceptions import ValidationError


def validate_person_name(value):

    value = value.strip()

    valid = all(
        category(char).startswith(("L", "M"))
        or char in " -'’"
        for char in value
    )

    has_letter = any(
        char.isalpha()
        for char in value
    )

    if not valid or not has_letter:

        raise ValidationError(
            "Please enter a valid name."
        )

    return value