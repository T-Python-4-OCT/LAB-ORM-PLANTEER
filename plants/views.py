
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .models import Plant
from .forms import PlantForm, CommentForm


def all_plants(request):
    category = request.GET.get("category", "")
    is_edible = request.GET.get("is_edible", "")

    plants = Plant.objects.all()

    if category in Plant.Category.values:
        plants = plants.filter(category=category)
    else:
        category = ""

    if is_edible in ["true", "false"]:
        plants = plants.filter(is_edible=(is_edible == "true"))
    else:
        is_edible = ""

    plants = plants.order_by("-created_at", "-id")

    context = {
        "plants": plants,
        "categories": Plant.Category.choices,
        "selected_category": category,
        "selected_edible": is_edible,
    }

    return render(request, "plants/all_plants.html", context)


def search_plants(request):
    query = request.GET.get("q", "").strip()

    plants = Plant.objects.none()

    if query:
        plants = Plant.objects.filter(
            Q(name__icontains=query)
            | Q(about__icontains=query)
            | Q(used_for__icontains=query)
        ).order_by("name")

    return render(
        request,
        "plants/search.html",
        {"plants": plants, "query": query}
    )


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(
        id=plant.id
    ).order_by("-created_at")[:3]

    comments = plant.comments.order_by("-created_at", "-id")

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.plant = plant
            comment.save()

            return redirect("plants:detail", plant_id=plant.id)
    else:
        form = CommentForm()

    context = {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments,
        "form": form,
    }

    return render(request, "plants/plant_detail.html", context)


def add_plant(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)

        if form.is_valid():
            plant = form.save()
            return redirect("plants:detail", plant_id=plant.id)
    else:
        form = PlantForm()

    return render(request, "plants/add_plant.html", {"form": form})


def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)

        if form.is_valid():
            form.save()
            return redirect("plants:detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(
        request,
        "plants/update_plant.html",
        {"form": form, "plant": plant}
    )


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect("plants:all")

    return render(
        request,
        "plants/delete_plant.html",
        {"plant": plant}
    )
