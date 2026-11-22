from django.core.paginator import Paginator

from .models import Plant

SORT_OPTIONS = {
    "newest": ("-created_at", "-id"),
    "oldest": ("created_at", "id"),
    "az": ("name", "id"),
    "za": ("-name", "id"),
}


def filter_and_paginate(request, plants, per_page=9):

    selected_categories = request.GET.getlist("category")
    is_edible = request.GET.get("is_edible", "")
    sort = request.GET.get("sort", "newest")


    selected_categories = [
        category
        for category in selected_categories
        if category in Plant.Category.values
    ]


    if selected_categories:
        plants = plants.filter(
            category__in=selected_categories
        )


    if is_edible == "yes":
        plants = plants.filter(is_edible=True)

    elif is_edible == "no":
        plants = plants.filter(is_edible=False)

    else:
        is_edible = ""


    if sort not in SORT_OPTIONS:
        sort = "newest"

    plants = plants.order_by(*SORT_OPTIONS[sort])


    paginator = Paginator(plants, per_page)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    page_range = paginator.get_elided_page_range( # type: ignore
        page_obj.number,
        on_each_side=2,
        on_ends=1
    )

    return {
        "page_obj": page_obj,
        "page_range": page_range,
        "categories": Plant.Category.choices,
        "selected_categories": selected_categories,
        "is_edible": is_edible,
        "sort": sort,
        "total_plants": paginator.count,
    }