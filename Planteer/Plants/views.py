from django.shortcuts import render
from .models import Plant


def all_plants(request):
    plants = Plant.objects.all()

    category = request.GET.get("category")
    is_edible = request.GET.get("is_edible")

    if category:
        plants = plants.filter(category=category)

    if is_edible == "true":
        plants = plants.filter(is_edible=True)
    elif is_edible == "false":
        plants = plants.filter(is_edible=False)

    context = {
        "plants": plants,
        "categories": Plant.Category.choices,
        "selected_category": category,
        "selected_edible": is_edible,
    }

    return render(request, "Plants/all_plants.html", context)


def add_plant(request):
    pass


def search_plants(request):
    pass


def plant_detail(request, plant_id):
    pass


def update_plant(request, plant_id):
    pass


def delete_plant(request, plant_id):
    pass