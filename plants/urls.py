from django.urls import path
from .views import plant_list

urlpatterns = [path("all/", plant_list, name="plant_list")]
