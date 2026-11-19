from django.urls import path

from . import views

app_name = "plants"

urlpatterns = [

    path(
        "all/",
        views.all_plants,
        name="all_plants"
    ),

    path(
        "search/",
        views.search,
        name="search"
    ),

    path(
        "<int:plant_id>/detail/",
        views.plant_detail,
        name="plant_detail"
    ),

]