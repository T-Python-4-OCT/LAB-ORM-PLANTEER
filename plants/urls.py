from django.urls import path

from . import views

app_name = "plants"

urlpatterns = [
    path("all/", views.all_plants_view, name="all_plants"),
    path("search/", views.search_view, name="search"),
    path("new/", views.plant_create_view, name="plant_create"),
    path("<int:plant_id>/detail/", views.plant_detail_view, name="plant_detail"),
    path("<int:plant_id>/update/", views.plant_update_view, name="plant_update"),
    path("<int:plant_id>/delete/", views.plant_delete_view, name="plant_delete"),
]
