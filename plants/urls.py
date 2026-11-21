from django.urls import path
from .views import plant_create, plant_delete, plant_detail, plant_list, plant_update

urlpatterns = [
    path("all/", plant_list, name="plant_list"),
    path("new/", plant_create, name="plant_create"),
    path("<int:plant_id>/detail/", plant_detail, name="plant_detail"),
    path("<int:plant_id>/update/", plant_update, name="plant_update"),
    path("<int:plant_id>/delete/", plant_delete, name="plant_delete"),
]
