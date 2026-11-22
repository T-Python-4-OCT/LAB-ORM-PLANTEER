from django.shortcuts import render
from django.http import HttpRequest
from plants.models import Plant


def home_view(request: HttpRequest):
    latest_plants = Plant.objects.order_by("-created_at")[:3]
    return render(request, "main/index.html", {"latest_plants": latest_plants})