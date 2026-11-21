from django.urls import path
from .views import plant_detail, plant_list

urlpatterns = [path("all/", plant_list, name="plant_list"), path("<int:plant_id>/detail/", plant_detail, name="plant_detail")]
