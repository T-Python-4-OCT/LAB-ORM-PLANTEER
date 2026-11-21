from django.shortcuts import render

STARTER_PLANTS = [
    {"id": 1, "name": "Date Palm", "scientific_name": "Phoenix dactylifera", "category": "Tree", "edible": True, "native_to": "Middle East and North Africa", "used_for": "Dates, shade, and traditional crafts.", "description": "A familiar desert tree, valued for its nourishing dates and generous shade.", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Date_palm_tree.jpg?width=1200"},
    {"id": 2, "name": "Olive", "scientific_name": "Olea europaea", "category": "Tree", "edible": True, "native_to": "Mediterranean Basin", "used_for": "Olive oil, table olives, and shade.", "description": "A long-lived evergreen with silvery leaves and fruit used for food and oil.", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Olea_europaea.jpg?width=1200"},
    {"id": 3, "name": "Lemon", "scientific_name": "Citrus limon", "category": "Fruit", "edible": True, "native_to": "Northeast India", "used_for": "Cooking, drinks, and preserves.", "description": "A fragrant citrus tree grown for bright, tart fruit and scented blossoms.", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Lemon_tree02.jpg?width=1200"},
    {"id": 4, "name": "Tomato", "scientific_name": "Solanum lycopersicum", "category": "Vegetable", "edible": True, "native_to": "Western South America", "used_for": "Salads, sauces, and fresh eating.", "description": "A sun-loving garden plant with juicy fruits and many varieties.", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/A_Tomato_plant.jpg?width=1200"},
]

def plant_list(request):
    return render(request, "plants/plant_list.html", {"plants": STARTER_PLANTS})

def plant_detail(request, plant_id):
    from django.http import Http404
    plant = next((item for item in STARTER_PLANTS if item["id"] == plant_id), None)
    if plant is None:
        raise Http404("Plant not found")
    related = [item for item in STARTER_PLANTS if item["category"] == plant["category"] and item["id"] != plant_id]
    return render(request, "plants/plant_detail.html", {"plant": plant, "related_plants": related})
