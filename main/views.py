from django.shortcuts import render
from plants.models import Plant

def home(request):
    plants = Plant.objects.all()[:3]
    return render(request, "main/home.html", {"plants": plants, "plant_count": Plant.objects.count()})
