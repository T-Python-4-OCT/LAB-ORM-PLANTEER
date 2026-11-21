from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods, require_safe

from .forms import CommentForm, PlantFilterForm, PlantForm
from .models import Plant


@require_safe
def all_plants(request):
    plants = Plant.objects.all()
    filters = PlantFilterForm(request.GET)
    if filters.is_valid():
        category = filters.cleaned_data["category"]
        is_edible = filters.cleaned_data["is_edible"]
        if category:
            plants = plants.filter(category=category)
        if is_edible is not None:
            plants = plants.filter(is_edible=is_edible)
    return render(request, "plants/all.html", {"plants": plants, "filters": filters})


@require_safe
def search(request):
    query = request.GET.get("q", "").strip()
    plants = Plant.objects.none()
    if query:
        plants = Plant.objects.filter(
            Q(name__icontains=query)
            | Q(about__icontains=query)
            | Q(used_for__icontains=query)
            | Q(name_ar__icontains=query)
            | Q(about_ar__icontains=query)
            | Q(used_for_ar__icontains=query)
        )
    return render(request, "plants/search.html", {"plants": plants, "query": query})


@require_http_methods(["GET", "POST"])
def detail(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    form = CommentForm(request.POST if request.method == "POST" else None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.plant = plant
        comment.save()
        return redirect(reverse("plants:detail", args=[plant.pk]) + "#comments")

    related = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]
    return render(
        request, "plants/detail.html", {"plant": plant, "related": related, "form": form}
    )


@require_http_methods(["GET", "POST"])
def edit_plant(request, plant_id=None):
    plant = get_object_or_404(Plant, pk=plant_id) if plant_id is not None else None
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES, instance=plant)
    else:
        form = PlantForm(instance=plant)

    if form.is_valid():
        saved_plant = form.save()
        message = _("Plant updated.") if plant else _("Plant added.")
        messages.success(request, message)
        return redirect("plants:detail", plant_id=saved_plant.pk)

    return render(request, "plants/form.html", {"form": form, "plant": plant})


@require_http_methods(["GET", "POST"])
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == "POST":
        name = plant.local_name
        plant.delete()
        messages.success(request, _("%(name)s was deleted.") % {"name": name})
        return redirect("plants:all")
    return render(request, "plants/delete.html", {"plant": plant})
