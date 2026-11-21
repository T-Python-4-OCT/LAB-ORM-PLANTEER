from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from .forms import CommentForm, PlantForm
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

def plant_search(request):
    query = request.GET.get("q", "").strip()
    plants = Plant.objects.none()
    if query:
        plants = Plant.objects.filter(
            Q(name__icontains=query)
            | Q(scientific_name__icontains=query)
            | Q(about__icontains=query)
            | Q(used_for__icontains=query)
        )
    return render(request, "plants/search.html", {"plants": plants, "query": query})

def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    comment_form = CommentForm(request.POST or None)
    if request.method == "POST" and comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.plant = plant
        comment.save()
        return redirect("plant_detail", plant_id=plant.pk)
    related = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]
    return render(request, "plants/plant_detail.html", {
        "plant": plant,
        "related_plants": related,
        "comment_form": comment_form,
        "comments": plant.comments.all(),
    })

def plant_create(request):
    form = PlantForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        plant = form.save()
        return redirect("plant_detail", plant_id=plant.pk)
    return render(request, "plants/plant_form.html", {"form": form, "title": "Add a plant", "submit_label": "Add plant"})

def plant_update(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    form = PlantForm(request.POST or None, request.FILES or None, instance=plant)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("plant_detail", plant_id=plant.pk)
    return render(request, "plants/plant_form.html", {"form": form, "plant": plant, "title": f"Edit {plant.name}", "submit_label": "Save changes"})

def plant_delete(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        plant.delete()
        return redirect("plant_list")
    return render(request, "plants/plant_confirm_delete.html", {"plant": plant})
