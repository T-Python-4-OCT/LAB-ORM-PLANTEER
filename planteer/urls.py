from django.urls import include, path
from main.views import home

urlpatterns = [path("", home, name="home"), path("plants/", include("plants.urls"))]
