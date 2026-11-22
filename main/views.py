from django.shortcuts import render

from plants.models import Plant


def home_view(request):
    # Show the 3 newest plants (the model's Meta.ordering is newest first)
    latest_plants = Plant.objects.all()[:3]
    return render(request, "main/home.html", {"plants": latest_plants})
