from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from ..models import Plant


def plant_list(request):
    plants = Plant.objects.select_related(
        "created_by"
    ).order_by("-created_at", "-id")

    category = request.GET.get("category", "")
    edible = request.GET.get("edible", "")

    if category:
        plants = plants.filter(category=category)

    if edible in ("yes", "no"):
        plants = plants.filter(
            is_edible=(edible == "yes")
        )

    paginator = Paginator(plants, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "plants/all.html", {
        "plants": page_obj,
        "page_obj": page_obj,
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
            | Q(about__icontains=query)
            | Q(used_for__icontains=query)
        ).order_by("-created_at", "-id")

    paginator = Paginator(plants, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "plants/search.html", {
        "plants": page_obj,
        "page_obj": page_obj,
        "query": query,
    })
