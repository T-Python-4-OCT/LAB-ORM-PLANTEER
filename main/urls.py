from django.urls import path
from .views import contact, contact_messages

urlpatterns = [path("", contact, name="contact"), path("messages/", contact_messages, name="contact_messages")]
