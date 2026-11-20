from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from ..models import Plant
from ..forms import PlantForm


@login_required
def plant_create(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)

        if form.is_valid():
            plant = form.save(commit=False)
            plant.created_by = request.user
            plant.save()

            return redirect("plant_detail", pk=plant.pk)

    else:
        form = PlantForm()

    return render(request, "plants/form.html", {
        "form": form,
        "page_title": "Add Plant",
        "submit_label": "Add Plant",
    })


@login_required
def plant_update(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    if not request.user.is_superuser:
        if plant.created_by_id != request.user.pk:
            raise PermissionDenied

    if request.method == "POST":
        form = PlantForm(
            request.POST,
            request.FILES,
            instance=plant
        )

        if form.is_valid():
            form.save()
            return redirect("plant_detail", pk=plant.pk)

    else:
        form = PlantForm(instance=plant)

    return render(request, "plants/form.html", {
        "form": form,
        "plant": plant,
        "page_title": "Edit Plant",
        "submit_label": "Save Changes",
    })


@login_required
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    if not request.user.is_superuser:
        if plant.created_by_id != request.user.pk:
            raise PermissionDenied

    if request.method == "POST":
        plant.delete()
        return redirect("plant_list")

    return render(request, "plants/delete.html", {
        "plant": plant,
    })
