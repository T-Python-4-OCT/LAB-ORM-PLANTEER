
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_home, name="dashboard_home"),
    path("plants/", views.dashboard_plants, name="dashboard_plants"),
    path("users/", views.dashboard_users, name="dashboard_users"),
    path("comments/", views.dashboard_comments, name="dashboard_comments"),
    path("comments/<int:pk>/delete/", views.dashboard_comment_delete, name="dashboard_comment_delete"),
    path("messages/", views.dashboard_messages, name="dashboard_messages"),
    path("messages/<int:pk>/delete/", views.dashboard_message_delete, name="dashboard_message_delete"),
]
