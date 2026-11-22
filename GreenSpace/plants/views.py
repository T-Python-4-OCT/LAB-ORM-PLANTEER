
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comment
from django.db.models import Q


def all_plants(request):
    plants = Plant.objects.all().order_by('-created_at')

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')

    if category:
        plants = plants.filter(category=category)

    if is_edible:
        plants = plants.filter(is_edible=is_edible == 'true')

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': Plant.CATEGORY_CHOICES,
        'selected_category': category,
        'selected_edible': is_edible,
    })


def add_plant(request):
    if request.method == 'POST':
        Plant.objects.create(
            name=request.POST.get('name'),
            scientific_name=request.POST.get('scientific_name'),
            description=request.POST.get('description'),
            category=request.POST.get('category'),
            is_edible=request.POST.get('is_edible') == 'on',
            sunlight=request.POST.get('sunlight'),
            water=request.POST.get('water'),
            image=request.FILES.get('image')
        )

        return redirect('all_plants')

    return render(request, 'plants/add.html')


def all_plants(request):

    plants = Plant.objects.all().order_by('-created_at')

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')

    if category:
        plants = plants.filter(category=category)

    if is_edible:
        plants = plants.filter(is_edible=is_edible == 'true')

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': Plant.CATEGORY_CHOICES,
        'selected_category': category,
        'selected_edible': is_edible,
    })
    
    
def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    comments = plant.comments.all().order_by('-created_at')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        content = request.POST.get('content')

        if full_name and content:
            Comment.objects.create(
                plant=plant,
                full_name=full_name,
                content=content
            )

            return redirect('plant_detail', plant_id=plant.id)

    return render(request, 'plants/detail.html', {
        'plant': plant,
        'related_plants': related_plants,
        'comments': comments,
    })


def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        plant.name = request.POST.get('name')
        plant.scientific_name = request.POST.get('scientific_name')
        plant.description = request.POST.get('description')
        plant.category = request.POST.get('category')
        plant.is_edible = request.POST.get('is_edible') == 'on'
        plant.sunlight = request.POST.get('sunlight')
        plant.water = request.POST.get('water')

        if request.FILES.get('image'):
            plant.image = request.FILES.get('image')

        plant.save()

        return redirect('plant_detail', plant_id=plant.id)

    return render(request, 'plants/update.html', {
        'plant': plant,
        'categories': Plant.CATEGORY_CHOICES
    })


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        plant.delete()
        return redirect('all_plants')

    return render(request, 'plants/delete.html', {
        'plant': plant
    })

def search_plants(request):
    query = request.GET.get('q', '').strip()

    plants = Plant.objects.none()

    if query:
        plants = Plant.objects.filter(
            Q(name__icontains=query) |
            Q(scientific_name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        ).order_by('name')

    return render(request, 'plants/search.html', {
        'plants': plants,
        'query': query
    })
