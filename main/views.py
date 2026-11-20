from django.shortcuts import render
from plants.views import STARTER_PLANTS

def home(request):
    return render(request, "main/home.html", {"plants": STARTER_PLANTS[:3], "plant_count": len(STARTER_PLANTS)})
