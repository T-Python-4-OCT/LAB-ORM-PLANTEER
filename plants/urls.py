from django.urls import path
from . import views
urlpatterns = [path('all/', views.listing, name='plant_list'), path('search/', views.listing, name='plant_search'), path('new/', views.edit, name='plant_new'), path('<int:plant_id>/detail/', views.detail, name='plant_detail'), path('<int:plant_id>/update/', views.edit, name='plant_update'), path('<int:plant_id>/delete/', views.delete, name='plant_delete')]
