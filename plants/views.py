from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CommentForm, PlantForm
from .models import Plant


def all_plants_view(request: HttpRequest):
    plants = Plant.objects.all()

    # Filtering by category
    category = request.GET.get("category", "")
    if category in Plant.Category.values:
        plants = plants.filter(category=category)

    # Filtering by is_edible
    is_edible = request.GET.get("is_edible", "")
    if is_edible == "yes":
        plants = plants.filter(is_edible=True)
    elif is_edible == "no":
        plants = plants.filter(is_edible=False)

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "categories": Plant.Category.choices,
        "selected_category": category,
        "selected_edible": is_edible,
    })


def plant_detail_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.plant = plant
            comment.save()
            return redirect("plants:plant_detail_view", plant_id=plant.id)
    else:
        comment_form = CommentForm()

    # Related plants: same category, excluding this plant
    related_plants = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[0:3]

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants,
        "comments": plant.comments.all(),
        "comment_form": comment_form,
    })


def add_plant_view(request: HttpRequest):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            return redirect("plants:plant_detail_view", plant_id=plant.id)
    else:
        form = PlantForm()

    return render(request, "plants/plant_form.html", {"form": form, "title": "Add New Plant"})


def update_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect("plants:plant_detail_view", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, "plants/plant_form.html", {
        "form": form,
        "plant": plant,
        "title": f"Update {plant.name}",
    })


@require_POST
def delete_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)
    plant.delete()
    return redirect("plants:all_plants_view")


def search_plants_view(request: HttpRequest):
    search = request.GET.get("search", "").strip()
    plants = Plant.objects.none()
    if search:
        plants = Plant.objects.filter(
            Q(name__icontains=search) | Q(about__icontains=search) | Q(used_for__icontains=search)
        )

    return render(request, "plants/search.html", {"plants": plants, "search": search})
