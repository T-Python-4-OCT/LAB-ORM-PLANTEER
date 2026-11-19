from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from .models import Plant

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
            return redirect("main:home")

    return render(request, "plants/add_plant.html", {
        "plant": plant,
        "errors": errors,
        "categories": Plant.Category.choices,
    })


def search(request: HttpRequest):
    return render(request, "plants/search.html")