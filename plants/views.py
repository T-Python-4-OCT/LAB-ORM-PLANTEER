from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PlantForm
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

    return render(request, "plants/all_plants.html", {
        "plants": plants,
        "selected_category": category or "",
        "selected_is_edible": is_edible or "",
    })


def add_plant(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("all_plants")
    else:
        form = PlantForm()

    return render(request, "plants/plant_form.html", {"form": form})


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.plant = plant
            comment.save()
            return redirect("plant_detail", plant_id=plant.id)
    else:
        comment_form = CommentForm()

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)

    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related_plants,
        "comment_form": comment_form,
    })
# Search plants by name.
def search_plants(request):
    query = request.GET.get("q", "").strip()

    if query:
        plants = Plant.objects.filter(name__icontains=query).order_by("name")
    else:
        plants = Plant.objects.all().order_by("name")

    return render(request, "plants/search_results.html", {
        "plants": plants,
        "query": query,
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
        "plant": plant,
    })
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    # Delete only after the confirmation form is submitted.
    if request.method == "POST":
       image = plant.image
       plant.delete()

       if image and not Plant.objects.filter(image=image.name).exists():
           image.delete(save=False)

       return redirect("all_plants")

    return render(request, "plants/plant_confirm_delete.html", {
        "plant": plant,
    })