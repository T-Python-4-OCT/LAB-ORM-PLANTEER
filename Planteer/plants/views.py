from django.contrib import messages
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PlantForm
from .models import Plant


# Shared catalogue controls for the all-plants and search pages.
def _filtered_plants(request, *, search=False):
    """Apply the shared category, edibility, search, and sort controls."""
    plants = Plant.objects.annotate(rating_average=Avg("comments__rating"))
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    edible = request.GET.get("is_edible", "")
    sort = request.GET.get("sort", "name")

    if search and query:
        plants = plants.filter(
            Q(name__icontains=query)
            | Q(about__icontains=query)
            | Q(used_for__icontains=query)
            | Q(category__icontains=query)
        )
    if category in Plant.Category.values:
        plants = plants.filter(category=category)
    if edible in {"yes", "no"}:
        plants = plants.filter(is_edible=(edible == "yes"))

    sort_fields = {
        "name": "name",
        "-name": "-name",
        "newest": "-created_at",
        "oldest": "created_at",
        "rating": "-rating_average",
    }
    plants = plants.order_by(sort_fields.get(sort, "name"), "name")
    return plants, {
        "query": query,
        "selected_category": category,
        "selected_edible": edible,
        "selected_sort": sort,
        "categories": Plant.Category.choices,
    }


def home(request):
    plants = Plant.objects.annotate(rating_average=Avg("comments__rating"))[:6]
    return render(request, "plants/home.html", {"plants": plants})


def plant_list(request):
    plants, filters = _filtered_plants(request)
    return render(request, "plants/plant_list.html", {"plants": plants, **filters})


def search(request):
    plants, filters = _filtered_plants(request, search=True)
    return render(request, "plants/search.html", {"plants": plants, **filters})


def plant_detail(request, plant_id):
    plant = get_object_or_404(
        Plant.objects.annotate(rating_average=Avg("comments__rating")),
        pk=plant_id,
    )
    related_plants = (
        Plant.objects.filter(category=plant.category)
        .exclude(pk=plant.pk)
        .annotate(rating_average=Avg("comments__rating"))[:3]
    )
    comments = plant.comments.all()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.plant = plant
            comment.save()
            messages.success(request, "Your review has been added.")
            return redirect("plants:detail", plant_id=plant.pk)
    else:
        form = CommentForm()
    return render(
        request,
        "plants/plant_detail.html",
        {
            "plant": plant,
            "related_plants": related_plants,
            "comments": comments,
            "comment_form": form,
        },
    )


def plant_create(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            messages.success(request, f"{plant.name} has been added.")
            return redirect("plants:detail", plant_id=plant.pk)
    else:
        form = PlantForm()
    return render(
        request,
        "plants/plant_form.html",
        {"form": form, "page_title": "Add a plant", "submit_label": "Add plant"},
    )


def plant_update(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, f"{plant.name} has been updated.")
            return redirect("plants:detail", plant_id=plant.pk)
    else:
        form = PlantForm(instance=plant)
    return render(
        request,
        "plants/plant_form.html",
        {
            "form": form,
            "plant": plant,
            "page_title": "Edit plant",
            "submit_label": "Save changes",
        },
    )


def plant_delete(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        name = plant.name
        plant.delete()
        messages.success(request, f"{name} has been deleted.")
        return redirect("plants:all")
    return render(request, "plants/plant_confirm_delete.html", {"plant": plant})
