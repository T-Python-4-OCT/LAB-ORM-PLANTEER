
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from ..models import Plant
from ..forms import PlantForm, PlantImageFormSet


@login_required
def plant_create(request):
    plant = Plant()

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)

        image_formset = PlantImageFormSet(
            request.POST,
            request.FILES,
            instance=plant,
            prefix="images",
        )

        if form.is_valid() and image_formset.is_valid():
            with transaction.atomic():
                plant = form.save(commit=False)
                plant.created_by = request.user
                plant.save()

                image_formset.instance = plant
                image_formset.save()

            return redirect("plant_detail", pk=plant.pk)
    else:
        form = PlantForm()

        image_formset = PlantImageFormSet(
            instance=plant,
            prefix="images",
        )

    return render(request, "plants/form.html", {
        "form": form,
        "image_formset": image_formset,
        "page_title": "Add Plant",
        "submit_label": "Add Plant",
    })


@login_required
def plant_update(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    if not (
        request.user.is_staff
        or plant.created_by_id == request.user.pk
    ):
        raise PermissionDenied

    if request.method == "POST":
        form = PlantForm(
            request.POST,
            request.FILES,
            instance=plant,
        )

        image_formset = PlantImageFormSet(
            request.POST,
            request.FILES,
            instance=plant,
            prefix="images",
        )

        if form.is_valid() and image_formset.is_valid():
            with transaction.atomic():
                form.save()
                image_formset.save()

            return redirect("plant_detail", pk=plant.pk)

    else:
        form = PlantForm(instance=plant)

        image_formset = PlantImageFormSet(
            instance=plant,
            prefix="images",
        )

    return render(request, "plants/form.html", {
        "form": form,
        "image_formset": image_formset,
        "plant": plant,
        "page_title": "Edit Plant",
        "submit_label": "Save Changes",
    })


@login_required
def plant_delete(request, pk):
    plant = get_object_or_404(Plant, pk=pk)

    if not (
        request.user.is_staff
        or plant.created_by_id == request.user.pk
    ):
        raise PermissionDenied

    if request.method == "POST":
        plant.delete()
        return redirect("plant_list")

    return render(request, "plants/delete.html", {
        "plant": plant,
    })
