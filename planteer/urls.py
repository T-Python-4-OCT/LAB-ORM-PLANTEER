from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from main.views import home

urlpatterns = [path("", home, name="home"), path("plants/", include("plants.urls")), path("contact/", include("main.urls"))]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
