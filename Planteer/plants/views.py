from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm, PlantForm
from .models import Plant

RELATED_PLANTS_LIMIT = 3           # how many related plants the detail page shows
EDIBLE_FILTERS = {"yes": True, "no": False}  # ?is_edible=yes / ?is_edible=no


def all_plants(request):
    """All plants — can be filtered by category (?category=herb) and is_edible (?is_edible=yes)."""
    # order_by is needed: Meta.ordering is ignored in queries that use annotate(Count)
    plants = Plant.objects.annotate(comments_count=Count("comments")).order_by("-created_at")

    category = request.GET.get("category", "")
    if category in Plant.Category.values:
        plants = plants.filter(category=category)
    else:
        category = ""

    is_edible = request.GET.get("is_edible", "")
    if is_edible in EDIBLE_FILTERS:
        plants = plants.filter(is_edible=EDIBLE_FILTERS[is_edible])
    else:
        is_edible = ""

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "categories": Plant.Category.choices,
        "current_category": category,
        "current_is_edible": is_edible,
        "is_filtered": bool(category or is_edible),
    })


def render_plant_detail(request, plant, comment_form):
    """Shared by plant_detail and add_comment (when the comment form has errors)."""
    # related plants: same category, without the plant itself (filter + exclude)
    related_plants = (Plant.objects.filter(category=plant.category)
                      .exclude(pk=plant.pk)
                      .annotate(comments_count=Count("comments"))
                      .order_by("-created_at")[:RELATED_PLANTS_LIMIT])
    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "comments": plant.comments.all(),   # every comment whose plant_id == plant.id
        "comment_form": comment_form,
        "related_plants": related_plants,
    })


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    return render_plant_detail(request, plant, CommentForm())


def add_plant(request):
    """Add page: empty form (GET) or save the new plant (POST)."""
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)  # request.FILES carries the uploaded image
        if form.is_valid():
            plant = form.save()
            messages.success(request, f"“{plant.name}” was added to Planteer.")
            return redirect("plants:plant_detail", plant_id=plant.id)
    else:
        form = PlantForm()
    return render(request, "plants/plant_form.html", {"form": form, "is_update": False})


def update_plant(request, plant_id):
    """Update page: the same form, filled with the plant (instance=plant)."""
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()  # no new image chosen -> the current image is kept
            messages.success(request, f"“{plant.name}” was updated.")
            return redirect("plants:plant_detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, "plants/plant_form.html", {"form": form, "plant": plant, "is_update": True})


def delete_plant(request, plant_id):
    """GET shows a confirmation page, POST deletes the plant (and its comments)."""
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        name = plant.name
        plant.delete()
        messages.success(request, f"“{name}” was deleted.")
        return redirect("plants:all_plants")
    return render(request, "plants/plant_delete.html", {"plant": plant})


def search(request):
    """Search by name, about or used_for: /plants/search/?q=mint"""
    query = request.GET.get("q", "").strip()
    results = Plant.objects.none()
    if query:
        results = (Plant.objects.filter(Q(name__icontains=query) | Q(about__icontains=query)
                                        | Q(used_for__icontains=query))
                   .annotate(comments_count=Count("comments"))
                   .order_by("-created_at"))
    return render(request, "plants/search.html", {"query": query, "results": results})


def add_comment(request, plant_id):
    """Saves a visitor's comment and links it to its plant (POST only)."""
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method != "POST":
        return redirect("plants:plant_detail", plant_id=plant.id)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)  # build the comment without saving it
        comment.plant = plant              # link it to the plant (fills plant_id)
        comment.save()
        messages.success(request, f"Thanks {comment.full_name}, your comment was posted.")
        return redirect(reverse("plants:plant_detail", args=[plant.id]) + "#comments")

    return render_plant_detail(request, plant, form)  # show the errors on the same page
