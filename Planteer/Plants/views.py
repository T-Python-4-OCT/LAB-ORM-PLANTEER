from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comment
from django.db.models import Q
from django.http import JsonResponse

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

    if request.method == "POST":
        Plant.objects.create(
            name=request.POST.get("name"),
            category=request.POST.get("category"),
            about=request.POST.get("about"),
            used_for=request.POST.get("used_for"),
            image=request.FILES.get("image"),
            is_edible=request.POST.get("is_edible") == "on"
        )

        return redirect("all_plants")

    context = {
        "categories": Plant.Category.choices,
    }

    return render(request, "Plants/add_plant.html", context)



def search_plants(request):
    query = request.GET.get("q", "").strip()

    if request.GET.get("live") == "1":
        plants = Plant.objects.filter(
            name__istartswith=query
        ) if query else Plant.objects.none()

        results = [
            {
                "id": plant.id,
                "name": plant.name,
                "category": plant.category,
                "image": plant.image.url,
            }
            for plant in plants
        ]

        return JsonResponse({"plants": results})

    plants = Plant.objects.filter(
        Q(name__icontains=query) |
        Q(about__icontains=query) |
        Q(used_for__icontains=query)
    ) if query else Plant.objects.all()

    return render(request, "Plants/search_plants.html", {
        "plants": plants,
        "query": query,
    })


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        content = request.POST.get("content")

        if full_name and content:
            Comment.objects.create(
                plant=plant,
                full_name=full_name,
                content=content
            )

        return redirect("plant_detail", plant_id=plant.id)

    comments = plant.comments.all().order_by("-created_at")

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    context = {
        "plant": plant,
        "comments": comments,
        "related_plants": related_plants,
    }

    return render(request, "Plants/plant_detail.html", context)



def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.name = request.POST.get("name")
        plant.category = request.POST.get("category")
        plant.about = request.POST.get("about")
        plant.used_for = request.POST.get("used_for")
        plant.is_edible = request.POST.get("is_edible") == "on"

        if request.FILES.get("image"):
            plant.image = request.FILES.get("image")

        plant.save()

        return redirect("plant_detail", plant_id=plant.id)

    context = {
        "plant": plant,
        "categories": Plant.Category.choices,
    }

    return render(request, "Plants/update_plant.html", context)




def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect("all_plants")

    return render(request, "Plants/delete_plant.html", {
        "plant": plant,
    })
