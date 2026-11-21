from django.shortcuts import get_object_or_404, render
from .models import Plant

def plant_list(request):
    plants = Plant.objects.all()
    category = request.GET.get("category", "")
    edible = request.GET.get("is_edible", "")
    if category in Plant.Category.values:
        plants = plants.filter(category=category)
    if edible in ("true", "false"):
        plants = plants.filter(is_edible=(edible == "true"))
    return render(request, "plants/plant_list.html", {
        "plants": plants,
        "categories": Plant.Category.choices,
        "selected_category": category,
        "selected_edible": edible,
    })

def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    related = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]
    return render(request, "plants/plant_detail.html", {"plant": plant, "related_plants": related})
