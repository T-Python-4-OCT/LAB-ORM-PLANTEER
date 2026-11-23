from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PlantForm
from .models import Plant


def plant_detail_view(request, plant_id):
    # Returns a 404 page instead of crashing if the plant does not exist
    plant = get_object_or_404(Plant, pk=plant_id)
    return render(request, "plants/plant_detail.html", {"plant": plant})


def plant_create_view(request):
    if request.method == "POST":
        # request.FILES is needed because the form uploads an image
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            messages.success(request, f'"{plant.name}" was added successfully.')
            return redirect("plants:plant_detail", plant_id=plant.id)
    else:
        form = PlantForm()  # empty form for GET requests

    return render(request, "plants/plant_form.html", {"form": form, "is_update": False})


def plant_update_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == "POST":
        # instance=plant tells the form to UPDATE this plant instead of creating a new one
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{plant.name}" was updated successfully.')
            return redirect("plants:plant_detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)  # form pre-filled with the plant's data

    return render(request, "plants/plant_form.html", {"form": form, "plant": plant, "is_update": True})


def plant_delete_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    # Only delete on POST. A GET request just shows the confirmation page.
    if request.method == "POST":
        name = plant.name
        plant.delete()
        messages.success(request, f'"{name}" was deleted.')
        return redirect("main:home")

    return render(request, "plants/plant_confirm_delete.html", {"plant": plant})
