from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PlantForm
from .models import Plant


def all_plants_view(request: HttpRequest):
    plants = Plant.objects.all().order_by("-created_at")

    category = request.GET.get("category", "")
    is_edible = request.GET.get("is_edible", "")

    if category:
        plants = plants.filter(category=category)

    if is_edible == "yes":
        plants = plants.filter(is_edible=True)
    elif is_edible == "no":
        plants = plants.filter(is_edible=False)

    context = {
        "plants": plants,
        "categories": Plant.Category.choices,
        "selected_category": category,
        "selected_edible": is_edible,
    }
    return render(request, "plants/all_plants.html", context)


def plant_detail_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, id=plant_id)
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]
    comments = plant.comment_set.order_by("-created_at")

    context = {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments,
        "comment_form": CommentForm(),
    }
    return render(request, "plants/plant_detail.html", context)


def new_plant_view(request: HttpRequest):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            return redirect("plants:plant_detail_view", plant_id=plant.id)
    else:
        form = PlantForm()

    context = {"form": form, "title": "Add New Plant", "button": "Add Plant"}
    return render(request, "plants/plant_form.html", context)


def update_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect("plants:plant_detail_view", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    context = {"form": form, "plant": plant, "title": "Update Plant", "button": "Save Changes"}
    return render(request, "plants/plant_form.html", context)


def delete_plant_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect("plants:all_plants_view")

    return redirect("plants:plant_detail_view", plant_id=plant.id)


def add_comment_view(request: HttpRequest, plant_id: int):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.plant = plant
            comment.save()

    return redirect("plants:plant_detail_view", plant_id=plant.id)


def search_view(request: HttpRequest):
    query = request.GET.get("search", "").strip()

    if query:
        plants = Plant.objects.filter(name__icontains=query).order_by("-created_at")
    else:
        plants = Plant.objects.none()

    return render(request, "plants/search.html", {"plants": plants, "query": query})
