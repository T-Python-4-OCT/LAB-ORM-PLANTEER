from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from .models import Plant, Comment


def all_plants(request: HttpRequest):
    category = request.GET.get("category", "")
    edible = request.GET.get("edible", "")

    plants = Plant.objects.all()

    if category in Plant.Category.values:
        plants = plants.filter(category=category)
    else:
        category = ""

    if edible == "yes":
        plants = plants.filter(is_edible=True)
    elif edible == "no":
        plants = plants.filter(is_edible=False)
    else:
        edible = ""

    plants = plants.order_by("-created_at")

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "categories": Plant.Category.choices,
        "category": category,
        "edible": edible,
    })


def plant_detail(request: HttpRequest, plant_id: int):
    plant = Plant.objects.get(id=plant_id)
    comments = plant.comment_set.all().order_by("-created_at")
    related_plants = (
        Plant.objects.filter(category=plant.category)
        .exclude(id=plant.id)
        .order_by("-created_at")[:3]
    )
    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "comments": comments,
        "related_plants": related_plants,
    })


def save_plant(request: HttpRequest, plant: Plant) -> dict:
    plant.name = request.POST.get("name", "").strip()
    plant.about = request.POST.get("about", "").strip()
    plant.used_for = request.POST.get("used_for", "").strip()
    plant.category = request.POST.get("category", "")
    plant.is_edible = request.POST.get("is_edible") == "yes"
    if "image" in request.FILES:
        plant.image = request.FILES["image"]

    try:
        plant.full_clean()
    except ValidationError as e:
        errors = {}
        for field, messages in e.message_dict.items():
            errors[field] = messages[0]
        return errors

    plant.save()
    return {}


def add_plant(request: HttpRequest):
    plant = Plant()
    errors = {}

    if request.method == "POST":
        errors = save_plant(request, plant)
        if not errors:
            return redirect("plants:plant_detail", plant_id=plant.id)

    return render(request, "plants/add_plant.html", {
        "plant": plant,
        "errors": errors,
        "categories": Plant.Category.choices,
    })


def update_plant(request: HttpRequest, plant_id: int):
    plant = Plant.objects.get(id=plant_id)
    errors = {}

    if request.method == "POST":
        errors = save_plant(request, plant)
        if not errors:
            return redirect("plants:plant_detail", plant_id=plant.id)

    return render(request, "plants/update_plant.html", {
        "plant": plant,
        "errors": errors,
        "categories": Plant.Category.choices,
    })


def delete_plant(request: HttpRequest, plant_id: int):
    plant = Plant.objects.get(id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect("plants:all_plants")

    return redirect("plants:plant_detail", plant_id=plant.id)


def add_comment(request: HttpRequest, plant_id: int):
    plant = Plant.objects.get(id=plant_id)

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        content = request.POST.get("content", "").strip()
        if full_name and content:
            comment = Comment(plant=plant, full_name=full_name, content=content)
            comment.save()

    return redirect("plants:plant_detail", plant_id=plant.id)


def search(request: HttpRequest):
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")

    if category not in Plant.Category.values:
        category = ""

    plants = Plant.objects.none()
    searched = bool(q or category)

    if searched:
        plants = Plant.objects.all()
        if q:
            plants = plants.filter(name__icontains=q)
        if category:
            plants = plants.filter(category=category)
        plants = plants.order_by("name")

    return render(request, "plants/search.html", {
        "plants": plants,
        "q": q,
        "category": category,
        "categories": Plant.Category.choices,
        "searched": searched,
    })