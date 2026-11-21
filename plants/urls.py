from django.urls import path

from plants import views

app_name = "plants"

urlpatterns = [
    path("all/", views.all_plants, name="all"),
    path("<int:plant_id>/detail/", views.plant_detail, name="detail"),
    path("new/", views.new_plant, name="new"),
    path("<int:plant_id>/update/", views.update_plant, name="update"),
    path("<int:plant_id>/delete/", views.delete_plant, name="delete"),
    path("search/", views.search, name="search"),
]
