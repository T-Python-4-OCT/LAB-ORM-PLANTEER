from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comment

# Create your views here.


def all_plants_view(request):
    plants = Plant.objects.all().order_by("-created_at")

    category = request.GET.get("category", "")
    is_edible = request.GET.get("is_edible", "")

    if category:
        plants = plants.filter(category=category)

    if is_edible == "true":
        plants = plants.filter(is_edible=True)
    elif is_edible == "false":
        plants = plants.filter(is_edible=False)

    context = {
        "plants": plants,
        "categories": Plant.CategoryChoices.choices,
        "selected_category": category,
        "selected_edible": is_edible,
    }
    return render(request, "plants/all_plants.html", context)


def add_plant_view(request):
    if request.method == "POST":
        Plant.objects.create(
            name=request.POST["name"],
            about=request.POST["about"],
            used_for=request.POST["used_for"],
            image=request.FILES["image"],
            category=request.POST["category"],
            is_edible="is_edible" in request.POST,
        )
        return redirect("plants:all")

    return render(request, "plants/add_plant.html", {"categories": Plant.CategoryChoices.choices})


def plant_detail_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        Comment.objects.create(
            plant=plant,
            full_name=request.POST["full_name"],
            content=request.POST["content"],
        )
        return redirect("plants:detail", plant_id=plant.id)

    comments = plant.comments.all().order_by("-created_at")
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]

    context = {
        "plant": plant,
        "comments": comments,
        "related_plants": related_plants,
    }
    return render(request, "plants/plant_detail.html", context)

def update_plant_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]
        plant.category = request.POST["category"]
        plant.is_edible = "is_edible" in request.POST

        if "image" in request.FILES:
            plant.image = request.FILES["image"]

        plant.save()
        return redirect("plants:detail", plant_id=plant.id)

    context = {
        "plant": plant,
        "categories": Plant.CategoryChoices.choices,
    }
    return render(request, "plants/update_plant.html", context)


def delete_plant_view(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect("plants:all")

    return redirect("plants:detail", plant_id=plant.id)

def search_view(request):
    query = request.GET.get("q", "").strip()
    plants = []

    if query:
        plants = Plant.objects.filter(name__icontains=query).order_by("-created_at")

    context = {
        "plants": plants,
        "query": query,
    }
    return render(request, "plants/search.html", context)
