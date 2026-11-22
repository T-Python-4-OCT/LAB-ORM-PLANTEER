from django.urls import path
from . import views

app_name = "plants"

urlpatterns = [
    path("all/", views.all_plants_view, name="all"),
    path("new/", views.add_plant_view, name="new"),
    path("<int:plant_id>/detail/", views.plant_detail_view, name="detail"),
    path("<int:plant_id>/update/", views.update_plant_view, name="update"),
    path("<int:plant_id>/delete/", views.delete_plant_view, name="delete"),
    path("search/", views.search_view, name="search"),
]