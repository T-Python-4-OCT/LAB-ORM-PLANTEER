from django.shortcuts import render

STARTER_PLANTS = [
    {"id": 1, "name": "Date Palm", "scientific_name": "Phoenix dactylifera", "category": "Tree", "edible": True, "description": "A familiar desert tree, valued for its nourishing dates and generous shade.", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Date_palm_tree.jpg?width=1200"},
    {"id": 2, "name": "Olive", "scientific_name": "Olea europaea", "category": "Tree", "edible": True, "description": "A long-lived evergreen with silvery leaves and fruit used for food and oil.", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Olea_europaea.jpg?width=1200"},
    {"id": 3, "name": "Lemon", "scientific_name": "Citrus limon", "category": "Fruit", "edible": True, "description": "A fragrant citrus tree grown for bright, tart fruit and scented blossoms.", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Lemon_tree02.jpg?width=1200"},
    {"id": 4, "name": "Tomato", "scientific_name": "Solanum lycopersicum", "category": "Vegetable", "edible": True, "description": "A sun-loving garden plant with juicy fruits and many varieties.", "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/A_Tomato_plant.jpg?width=1200"},
]

def plant_list(request):
    return render(request, "plants/plant_list.html", {"plants": STARTER_PLANTS})
