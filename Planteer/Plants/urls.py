
from django.urls import path
from . import views

urlpatterns = [
    # All Plants
    path("all/", views.all_plants, name="all_plants"),

    # Add New Plant
    path("new/", views.add_plant, name="add_plant"),

    # Search Plants
    path("search/", views.search_plants, name="search_plants"),

    # Plant Details
    path("<int:plant_id>/detail/", views.plant_detail, name="plant_detail"),

    # Update Plant
    path("<int:plant_id>/update/", views.update_plant, name="update_plant"),

    # Delete Plant
    path("<int:plant_id>/delete/", views.delete_plant, name="delete_plant"),
]
