
from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comment
from .forms import PlantForm, CommentForm


def all_plants(request):
    plants = Plant.objects.all()

    category = request.GET.get('category')
    is_edible = request.GET.get('is_edible')

    if category:
        plants = plants.filter(category=category)

    if is_edible in ['true', 'false']:
        plants = plants.filter(is_edible=(is_edible == 'true'))

    context = {
        'plants': plants,
        'categories': Plant.CategoryChoices.choices,
        'selected_category': category,
        'selected_edible': is_edible,
    }

    return render(request, 'plants/all_plants.html', context)


def add_plant(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('all_plants')
    else:
        form = PlantForm()

    return render(request, 'plants/add_plant.html', {'form': form})



def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.plant = plant
            comment.save()

            return redirect('plant_detail', plant_id=plant.id)
    else:
        form = CommentForm()

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id)[:3]

    comments = Comment.objects.filter(
        plant=plant
    ).order_by('-created_at')

    context = {
        'plant': plant,
        'related_plants': related_plants,
        'comments': comments,
        'form': form,
    }

    return render(request, 'plants/plant_detail.html', context)

def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)

        if form.is_valid():
            form.save()
            return redirect('plant_detail', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)

    return render(request, 'plants/update_plant.html', {
        'form': form,
        'plant': plant,
    })


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        plant.delete()
        return redirect('all_plants')

    return render(request, 'plants/delete_plant.html', {
        'plant': plant,
    })

def search_plants(request):
    query = request.GET.get('q', '').strip()

    plants = Plant.objects.none()

    if query:
        plants = Plant.objects.filter(
            name__icontains=query
        )

    return render(request, 'plants/search.html', {
        'plants': plants,
        'query': query
    })
