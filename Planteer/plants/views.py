from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Plant, Comment


def all_plants_view(request: HttpRequest):

    plants = Plant.objects.order_by("-created_at")

    category = request.GET.get("category", "")
    if category:
        plants = plants.filter(category=category)

    edible = request.GET.get("edible", "")
    if edible == "yes":
        plants = plants.filter(is_edible=True)
    elif edible == "no":
        plants = plants.filter(is_edible=False)

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "plants_count": plants.count(),
        "categories": Plant.Category.choices,
        "category": category,
        "edible": edible,
    })


def plant_detail_view(request: HttpRequest, plant_id: int):

    plant = get_object_or_404(Plant, pk=plant_id)
    related_plants = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]
    comments = plant.comment_set.order_by("-created_at")

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments,
    })


def add_plant_view(request: HttpRequest):

    if request.method == "POST":
        new_plant = Plant(
            name=request.POST["name"],
            about=request.POST["about"],
            used_for=request.POST["used_for"],
            image=request.FILES["image"],
            category=request.POST["category"],
            is_edible="is_edible" in request.POST,
        )
        new_plant.save()

        return redirect("plants:plant_detail_view", plant_id=new_plant.id)

    return render(request, "plants/add_plant.html", {"categories": Plant.Category.choices})


def update_plant_view(request: HttpRequest, plant_id: int):

    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == "POST":
        plant.name = request.POST["name"]
        plant.about = request.POST["about"]
        plant.used_for = request.POST["used_for"]
        plant.category = request.POST["category"]
        plant.is_edible = "is_edible" in request.POST
        if "image" in request.FILES:
            plant.image = request.FILES["image"]
        plant.save()

        return redirect("plants:plant_detail_view", plant_id=plant.id)

    return render(request, "plants/update_plant.html", {"plant": plant, "categories": Plant.Category.choices})


def delete_plant_view(request: HttpRequest, plant_id: int):

    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == "POST":
        plant.image.delete(save=False)
        plant.delete()
        return redirect("plants:all_plants_view")

    return redirect("plants:plant_detail_view", plant_id=plant.id)


def search_view(request: HttpRequest):

    query = request.GET.get("q", "").strip()
    plants = []
    if query:
        plants = Plant.objects.filter(name__icontains=query).order_by("name")

    return render(request, "plants/search.html", {"plants": plants, "query": query})


def add_comment_view(request: HttpRequest, plant_id: int):

    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == "POST":
        new_comment = Comment(
            plant=plant,
            full_name=request.POST["full_name"],
            content=request.POST["content"],
        )
        new_comment.save()

    return redirect("plants:plant_detail_view", plant_id=plant.id)
