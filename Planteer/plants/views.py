from django.shortcuts import render, get_object_or_404, redirect
from .models import Plant, Comment
from django.db.models import Q
from .forms import PlantForm


def all_plants(request):
    plants = Plant.objects.all()

    category = request.GET.get("category", "")
    is_edible = request.GET.get("is_edible", "")
    sort = request.GET.get("sort", "newest")

    if category:
        plants = plants.filter(category=category)

    if is_edible == "true":
        plants = plants.filter(is_edible=True)
    elif is_edible == "false":
        plants = plants.filter(is_edible=False)

    if sort == "name":
        plants = plants.order_by("name")
    elif sort == "oldest":
        plants = plants.order_by("id")
    else:
        plants = plants.order_by("-id")

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "categories": Plant._meta.get_field("category").choices,
        "selected_category": category,
        "selected_edible": is_edible,
        "selected_sort": sort,
    })

def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    comments = plant.comments.all().order_by("-created_at")

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        content = request.POST.get("content", "").strip()

        if full_name and content and len(full_name) <= 100:
            Comment.objects.create(
                plant=plant,
                full_name=full_name,
                content=content
            )

            return redirect("plant_detail", plant_id=plant.id)

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments,
    })

def new_plant(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)

        if form.is_valid():
            plant = form.save()
            return redirect("plant_detail", plant_id=plant.id)
    else:
        form = PlantForm()

    return render(request, "plants/plant_form.html", {
        "form": form,
        "page_title": "Add New Plant",
        "button_text": "Add Plant",
    })


def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)

        if form.is_valid():
            form.save()
            return redirect("plant_detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, "plants/plant_form.html", {
        "form": form,
        "page_title": "Update Plant",
        "button_text": "Save Changes",
    })


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        plant.delete()
        return redirect("all_plants")

    return render(request, "plants/delete_plant.html", {
        "plant": plant,
    })


def search_plants(request):
    query = request.GET.get("q", "").strip()

    plants = Plant.objects.all().order_by("-created_at")

    if query:
        plants = plants.filter(
            Q(name__icontains=query)
            | Q(about__icontains=query)
            | Q(used_for__icontains=query)
        )

    plants = plants[:3]

    return render(request, "plants/search_plants.html", {
        "plants": plants,
        "query": query,
    })