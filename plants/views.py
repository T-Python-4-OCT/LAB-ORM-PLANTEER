from django.shortcuts import get_object_or_404, render

from .models import Plant


def plant_detail_view(request, plant_id):
    # Returns a 404 page instead of crashing if the plant does not exist
    plant = get_object_or_404(Plant, pk=plant_id)
    return render(request, "plants/plant_detail.html", {"plant": plant})
