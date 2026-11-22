from django.shortcuts import render, get_object_or_404

from ..models import Plant
from ..forms import CommentForm


def plant_detail(request, pk):
    plant = get_object_or_404(
        Plant.objects.select_related("created_by"),
        pk=pk
    )

    comments = plant.comments.select_related(
        "user"
    ).all()

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(
        pk=plant.pk
    ).order_by("-created_at")[:3]

    return render(request, "plants/detail.html", {
        "plant": plant,
        "images": plant.images.all(),
        "comments": comments,
        "related_plants": related_plants,
        "comment_form": CommentForm(),
    })
