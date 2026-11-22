from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from plants import views as plant_views

urlpatterns = [
    path("", plant_views.home, name="home"),
    path("plants/", include("plants.urls")),
    path("", include("main.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
