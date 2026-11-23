from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentForm, PlantForm
from .models import Plant


def all_plants_view(request):
    plants = Plant.objects.all()

    # Read the filters from the URL, e.g. /plants/all/?category=herb&is_edible=yes
    selected_category = request.GET.get("category", "")
    selected_edible = request.GET.get("is_edible", "")

    # Each filter is applied only if it has a valid value, so filters work together
    if selected_category in Plant.Category.values:
        plants = plants.filter(category=selected_category)

    if selected_edible == "yes":
        plants = plants.filter(is_edible=True)
    elif selected_edible == "no":
        plants = plants.filter(is_edible=False)

    context = {
        "plants": plants,
        "categories": Plant.Category.choices,
        "selected_category": selected_category,
        "selected_edible": selected_edible,
        "is_filtered": bool(selected_category or selected_edible),
    }
    return render(request, "plants/all_plants.html", context)


def search_view(request):
    query = request.GET.get("q", "").strip()
    results = Plant.objects.none()  # empty result until the user types something

    if query:
        # Q objects let us use OR: match the name OR the description
        results = Plant.objects.filter(Q(name__icontains=query) | Q(about__icontains=query))

    return render(request, "plants/search.html", {"query": query, "results": results})


def plant_detail_view(request, plant_id):
    # Returns a 404 page if the plant does not exist,
    # so nobody can comment on a plant that isn't there
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)  # build the comment but don't save yet
            comment.plant = plant                      # connect it to THIS plant
            comment.save()
            messages.success(request, "Thanks! Your comment was posted.")
            # Redirect after POST so refreshing the page doesn't post the comment twice
            return redirect(reverse("plants:plant_detail", args=[plant.id]) + "#comments")
    else:
        comment_form = CommentForm()

    # Related plants: same category, without the current plant, max 3
    related_plants = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]

    context = {
        "plant": plant,
        "comments": plant.comments.all(),  # newest first (Comment.Meta.ordering)
        "comment_form": comment_form,
        "related_plants": related_plants,
    }
    return render(request, "plants/plant_detail.html", context)


def plant_create_view(request):
    if request.method == "POST":
        # request.FILES is needed because the form uploads an image
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            messages.success(request, f'"{plant.name}" was added successfully.')
            return redirect("plants:plant_detail", plant_id=plant.id)
    else:
        form = PlantForm()  # empty form for GET requests

    return render(request, "plants/plant_form.html", {"form": form, "is_update": False})


def plant_update_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == "POST":
        # instance=plant tells the form to UPDATE this plant instead of creating a new one
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{plant.name}" was updated successfully.')
            return redirect("plants:plant_detail", plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)  # form pre-filled with the plant's data

    return render(request, "plants/plant_form.html", {"form": form, "plant": plant, "is_update": True})


def plant_delete_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    # Only delete on POST. A GET request just shows the confirmation page.
    if request.method == "POST":
        name = plant.name
        plant.delete()
        messages.success(request, f'"{name}" was deleted.')
        return redirect("main:home")

    return render(request, "plants/plant_confirm_delete.html", {"plant": plant})
