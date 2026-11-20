from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ..models import Plant
from ..forms import CommentForm


@login_required
@require_POST
def add_comment(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.plant = plant
        comment.user = request.user
        comment.save()

        return redirect("plant_detail", pk=plant.pk)

    comments = plant.comments.select_related("user").all()

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(pk=plant.pk).order_by("-created_at")[:3]

    return render(request, "plants/detail.html", {
        "plant": plant,
        "images": plant.images.all(),
        "comments": comments,
        "related_plants": related_plants,
        "comment_form": form,
    })
