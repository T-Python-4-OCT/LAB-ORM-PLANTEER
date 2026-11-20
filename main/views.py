
from django.shortcuts import render
from plants.models import Plant


def home(request):
    latest_plants = Plant.objects.order_by("-created_at")[:3]

    return render(
        request,
        "main/home.html",
        {"latest_plants": latest_plants}
    )
