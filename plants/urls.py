from django.urls import path

from . import views

app_name = "plants"

urlpatterns = [
    # More plant pages (all, new, update, delete, search) are added in the next stages
    path("<int:plant_id>/detail/", views.plant_detail_view, name="plant_detail"),
]
