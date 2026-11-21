"""Views of the plants app: all plants, detail (+ comments), new, update, delete, search."""

from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from plants.forms import CommentForm, PlantForm
from plants.models import Plant


def all_plants(request: HttpRequest) -> HttpResponse:
    """/plants/all/?category=fruit&is_edible=true  ->  filter by category and is_edible."""
    plants = Plant.objects.all().order_by("-created_at")

    category = request.GET.get("category", "")
    if category in Plant.Category.values:
        plants = plants.filter(category=category)

    is_edible = request.GET.get("is_edible", "")
    if is_edible == "true":
        plants = plants.filter(is_edible=True)
    elif is_edible == "false":
        plants = plants.filter(is_edible=False)

    context = {
        "plants": plants,
        "categories": Plant.Category.choices,
        "category": category,
        "is_edible": is_edible,
    }
    return render(request, "plants/all_plants.html", context)


def plant_detail(request: HttpRequest, plant_id: int) -> HttpResponse:
    """One plant, its comments (POST adds one), and related plants from the same category."""
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.plant = plant              # the relation: this comment belongs to this plant
            comment.save()
            return redirect("plants:detail", plant_id=plant.id)
    else:
        comment_form = CommentForm()

    # Related plants: same category (filter), without this plant (exclude), only 3
    related = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]
    comments = plant.comments.all().order_by("-created_at")

    context = {"plant": plant, "related": related, "comments": comments, "comment_form": comment_form}
    return render(request, "plants/plant_detail.html", context)


def new_plant(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            return redirect("plants:detail", plant_id=plant.id)
    else:
        form = PlantForm()
    return render(request, "plants/plant_form.html", {"form": form})


def update_plant(request: HttpRequest, plant_id: int) -> HttpResponse:
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            return redirect("plants:detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, "plants/plant_form.html", {"form": form, "plant": plant})


def delete_plant(request: HttpRequest, plant_id: int) -> HttpResponse:
    """GET asks to confirm, POST deletes the plant (and its comments, CASCADE)."""
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == "POST":
        plant.image.delete(save=False)     # remove the image file from the media folder
        plant.delete()
        return redirect("plants:all")
    return render(request, "plants/plant_delete.html", {"plant": plant})


def search(request: HttpRequest) -> HttpResponse:
    """/plants/search/?q=fruit  ->  plants whose name, about, used for, or category has the word."""
    q = request.GET.get("q", "").strip()
    plants = []
    if q:
        plants = Plant.objects.filter(
            Q(name__icontains=q) | Q(about__icontains=q) | Q(used_for__icontains=q) | Q(category__icontains=q)
        ).order_by("name")
    return render(request, "plants/search.html", {"q": q, "plants": plants})
