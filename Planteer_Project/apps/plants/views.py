from django.contrib import messages
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import CommentForm
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