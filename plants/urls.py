from django.urls import path

from . import views

app_name = "plants"

urlpatterns = [
    path("all/", views.all_plants, name="all"),
    path("search/", views.search, name="search"),
    path("new/", views.edit_plant, name="new"),
    path("<int:plant_id>/detail/", views.detail, name="detail"),
    path("<int:plant_id>/update/", views.edit_plant, name="update"),
    path("<int:plant_id>/delete/", views.delete_plant, name="delete"),
]
