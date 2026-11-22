from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CommentForm, PlantForm
from .models import Plant


def all_plants_view(request):
    plants = Plant.objects.all()

    category = request.GET.get('category', '')
    is_edible = request.GET.get('is_edible', '')

    if category in Plant.Category.values:
        plants = plants.filter(category=category)
    if is_edible == 'yes':
        plants = plants.filter(is_edible=True)
    elif is_edible == 'no':
        plants = plants.filter(is_edible=False)

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': Plant.Category.choices,
        'selected_category': category,
        'selected_edible': is_edible,
    })


def plant_detail_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.plant = plant
            comment.save()
            messages.success(request, 'Your comment was added.')
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        comment_form = CommentForm()

    related_plants = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
        'comments': plant.comments.all(),
        'comment_form': comment_form,
    })


def new_plant_view(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            messages.success(request, f'"{plant.name}" was added.')
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm()
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Add New Plant'})


def update_plant_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{plant.name}" was updated.')
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = PlantForm(instance=plant)
    return render(request, 'plants/plant_form.html', {'form': form, 'title': f'Update {plant.name}', 'plant': plant})


@require_POST
def delete_plant_view(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    name = plant.name
    plant.delete()
    messages.success(request, f'"{name}" was deleted.')
    return redirect('plants:all_plants')


def search_view(request):
    query = request.GET.get('q', '').strip()
    plants = Plant.objects.filter(name__icontains=query) if query else Plant.objects.none()
    return render(request, 'plants/search.html', {'plants': plants, 'query': query})
