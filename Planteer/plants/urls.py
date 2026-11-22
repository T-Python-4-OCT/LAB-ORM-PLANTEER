from django.urls import path

from . import views

app_name = "plants"

urlpatterns = [
    path("all/", views.plant_list, name="all"),
    path("search/", views.search, name="search"),
    path("new/", views.plant_create, name="new"),
    path("<int:plant_id>/detail/", views.plant_detail, name="detail"),
    path("<int:plant_id>/update/", views.plant_update, name="update"),
    path("<int:plant_id>/delete/", views.plant_delete, name="delete"),
]
