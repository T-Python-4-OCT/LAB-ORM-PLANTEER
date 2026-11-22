from django.contrib import messages
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import CommentForm, PlantForm
from .models import Plant
from .utils import filter_and_paginate


def all_plants(request):

    plants = Plant.objects.all()

    context = filter_and_paginate(request, plants)

    return render(
        request,
        "plants/all_plants.html",
        context
    )


@require_http_methods(["GET", "POST"])
def plant_detail(request, plant_id):


    plant = get_object_or_404(
        Plant,
        id=plant_id
    )


    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(
        id=plant.id
    ).order_by("?")[:3]

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.plant = plant

            comment.save()

            messages.success(
                request,
                "Your comment has been posted successfully."
            )

            url = reverse(
                "plants:plant_detail",
                kwargs={"plant_id": plant.id}
            )

            return redirect(f"{url}#comments")

    else:

        form = CommentForm()


    all_comments = plant.comments.all()

    comment_count = all_comments.count()

    show_all = request.GET.get("comments") == "all"

    if show_all:
        comments = all_comments
    else:
        comments = all_comments[:3]

    context = {
        "plant": plant,
        "related_plants": related_plants,
        "comments": comments,
        "comment_count": comment_count,
        "show_all": show_all,
        "form": form,
    }

    return render(
        request,
        "plants/plant_detail.html",
        context
    )
def search(request):

    query = request.GET.get("q", "").strip()

    plants = Plant.objects.all()

    if query:

        plants = plants.filter(

            Q(name__icontains=query) |
            Q(about__icontains=query) |
            Q(category__icontains=query) |
            Q(native_to__icontains=query)

        )

    context = filter_and_paginate(
        request,
        plants
    )

    context["query"] = query

    return render(
        request,
        "plants/search.html",
        context
    )
def get_management_url(request):

    url = reverse("plants:manage_plants")
    params = request.GET.urlencode()

    return f"{url}?{params}" if params else url


def render_management_page(
    request,
    form=None,
    modal_action=None,
    selected_plant=None
):

    plants = Plant.objects.all()

    query = request.GET.get("q", "").strip()

    if query:

        plants = plants.filter(
            Q(name__icontains=query) |
            Q(about__icontains=query) |
            Q(category__icontains=query) |
            Q(native_to__icontains=query)
        )

    context = filter_and_paginate(
        request,
        plants,
        per_page=10
    )

    params = request.GET.urlencode()

    context.update({
        "query": query,
        "form": form,
        "modal_action": modal_action,
        "selected_plant": selected_plant,
        "manage_url": reverse("plants:manage_plants"),
        "list_url": get_management_url(request),
        "query_suffix": f"?{params}" if params else "",
    })

    return render(
        request,
        "plants/manage_plants.html",
        context
    )

@require_http_methods(["GET"])
def manage_plants(request):

    return render_management_page(request)

@require_http_methods(["GET", "POST"])
def add_plant(request):

    if request.method == "POST":

        form = PlantForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            plant = form.save()

            messages.success(
                request,
                f"{plant.name} has been added successfully."
            )

            return redirect(get_management_url(request))

    else:

        form = PlantForm()

    return render_management_page(
        request,
        form=form,
        modal_action="add"
    )

@require_http_methods(["GET", "POST"])
def update_plant(request, plant_id):

    plant = get_object_or_404(
        Plant,
        id=plant_id
    )

    if request.method == "POST":

        form = PlantForm(
            request.POST,
            request.FILES,
            instance=plant
        )

        if form.is_valid():

            plant = form.save()

            messages.success(
                request,
                f"{plant.name} has been updated successfully."
            )

            return redirect(get_management_url(request))

    else:

        form = PlantForm(instance=plant)

    return render_management_page(
        request,
        form=form,
        modal_action="update",
        selected_plant=plant
    )

@require_http_methods(["GET", "POST"])
def delete_plant(request, plant_id):

    plant = get_object_or_404(
        Plant,
        id=plant_id
    )

    if request.method == "POST":

        plant_name = plant.name

        plant.delete()

        messages.success(
            request,
            f"{plant_name} has been deleted successfully."
        )

        return redirect(get_management_url(request))

    return render_management_page(
        request,
        modal_action="delete",
        selected_plant=plant
    )