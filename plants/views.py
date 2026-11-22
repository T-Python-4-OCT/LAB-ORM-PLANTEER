from django.shortcuts import render, redirect
from .models import Plant, Comment


def all_plants_view(request):
    plants = Plant.objects.order_by("-created_at")

    category = request.GET.get("category")
    edible = request.GET.get("edible")

    if category:
        plants = plants.filter(category=category)

    if edible == "yes":
        plants = plants.filter(is_edible=True)
    elif edible == "no":
        plants = plants.filter(is_edible=False)

    context = {
        "plants": plants,
        "categories": Plant.Category.choices,
        "selected_category": category,
        "selected_edible": edible,
    }
    return render(request, "plants/all_plants.html", context)


def plant_detail_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    related_plants = Plant.objects.filter(category=plant.category).exclude(id=plant.id)[:3]
    comments = Comment.objects.filter(plant=plant).order_by("-created_at")

    context = {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments,
    }
    return render(request, "plants/plant_detail.html", context)


def add_comment_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    if request.method == "POST":
        full_name = request.POST["full_name"].strip()
        content = request.POST["content"].strip()

        if len(full_name) >= 3 and len(content) >= 10:
            Comment.objects.create(
                plant=plant,
                full_name=full_name,
                content=content,
            )

    return redirect("plants:plant_detail", plant_id=plant.id)


def add_plant_view(request):
    if request.method == "POST":
        plant = Plant(
            name=request.POST["name"],
            about=request.POST["about"],
            used_for=request.POST["used_for"],
            native_to=request.POST["native_to"],
            category=request.POST["category"],
            is_edible="is_edible" in request.POST,
        )

        if "image" in request.FILES:
            plant.image = request.FILES["image"]

        plant.save()
        return redirect("plants:plant_detail", plant_id=plant.id)

    return render(request, "plants/add_plant.html", {
        "categories": Plant.Category.choices,
    })


def update_plant_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    if request.method == "POST":
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]
        plant.native_to = request.POST["native_to"]
        plant.category = request.POST["category"]
        plant.is_edible = "is_edible" in request.POST

        if "image" in request.FILES:
            plant.image = request.FILES["image"]

        plant.save()
        return redirect("plants:plant_detail", plant_id=plant.id)

    return render(request, "plants/update_plant.html", {
        "plant": plant,
        "categories": Plant.Category.choices,
    })


def delete_plant_view(request, plant_id):
    plant = Plant.objects.get(id=plant_id)

    if request.method == "POST":
        plant.delete()

    return redirect("plants:all_plants")


def search_view(request):
    query = request.GET.get("q", "")
    plants = []

    if query:
        plants = Plant.objects.filter(name__icontains=query)

    context = {
        "plants": plants,
        "query": query,
    }
    return render(request, "plants/search.html", context)