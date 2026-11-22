from django.urls import path

from . import views

app_name = "plants"
urlpatterns = [
    path("all/", views.catalog, name="catalog"),
    path("new/", views.create, name="create"),
    path("search/", views.search, name="search"),
    path("<int:plant_id>/detail/", views.detail, name="detail"),
    path("<int:plant_id>/update/", views.update, name="update"),
    path("<int:plant_id>/delete/", views.delete, name="delete"),
]
