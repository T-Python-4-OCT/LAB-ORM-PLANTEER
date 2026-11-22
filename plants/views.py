from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_safe, require_http_methods

from .forms import CommentForm, PlantForm
from .models import Plant


def matching_plants(query):
    return Plant.objects.filter(
        Q(name__icontains=query) | Q(about__icontains=query) | Q(used_for__icontains=query)
    )


@require_safe
def catalog(request):
    category = request.GET.get("category", "")
    edible = request.GET.get("is_edible", "")
    query = request.GET.get("q", "").strip()
    plants = matching_plants(query) if query else Plant.objects.all()
    if category in Plant.Category.values:
        plants = plants.filter(category=category)
    else:
        category = ""
    if edible in {"yes", "no"}:
        plants = plants.filter(is_edible=edible == "yes")
    else:
        edible = ""
    return render(request, "plants/catalog.html", {
        "plants": list(plants), "categories": Plant.Category.choices,
        "category": category, "edible": edible, "query": query,
    })


@require_safe
def search(request):
    query = request.GET.get("q", "").strip()
    plants = matching_plants(query) if query else Plant.objects.none()
    return render(request, "plants/search.html", {"plants": list(plants), "query": query})


@require_http_methods(["GET", "HEAD", "POST"])
def detail(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    form = CommentForm(request.POST) if request.method == "POST" else CommentForm()
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.plant = plant
        comment.save()
        messages.success(request, "Your comment was posted.")
        return redirect(plant.get_absolute_url() + "#comments")
    related = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]
    return render(request, "plants/detail.html", {
        "plant": plant, "form": form, "comments": plant.comments.all(), "related": related,
    })


def _plant_form(request, plant=None):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            record = form.save()
            messages.success(request, "Plant updated." if plant else "Plant added to the catalog.")
            return redirect(record)
    else:
        form = PlantForm(instance=plant)
    return render(request, "plants/form.html", {"form": form, "plant": plant})


@require_http_methods(["GET", "HEAD", "POST"])
def create(request):
    return _plant_form(request)


@require_http_methods(["GET", "HEAD", "POST"])
def update(request, plant_id):
    return _plant_form(request, get_object_or_404(Plant, pk=plant_id))


@require_http_methods(["GET", "HEAD", "POST"])
def delete(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        name = plant.name
        plant.delete()
        messages.success(request, f"{name} was deleted.")
        return redirect("plants:catalog")
    return render(request, "plants/delete.html", {"plant": plant})
