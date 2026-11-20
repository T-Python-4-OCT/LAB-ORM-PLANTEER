from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CommentForm, PlantForm
from .models import Plant


def all_plants(request):
    plants = Plant.objects.all()
    category = request.GET.get('category', '')
    edible = request.GET.get('is_edible', '')
    if category:
        plants = plants.filter(category=category)
    if edible == 'true':
        plants = plants.filter(is_edible=True)
    elif edible == 'false':
        plants = plants.filter(is_edible=False)
    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': Plant.Category.choices,
        'selected_category': category,
        'selected_edible': edible,
    })


def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.plant = plant
            comment.save()
            messages.success(request, 'Your comment was added.')
            return redirect('plants:plant_detail', plant_id=plant.id)
    else:
        form = CommentForm()
    related = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]
    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related': related,
        'comments': plant.comments.all(),
        'form': form,
    })


def add_plant(request):
    form = PlantForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        plant = form.save()
        messages.success(request, 'Plant added successfully.')
        return redirect('plants:plant_detail', plant_id=plant.id)
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Add Plant'})


def update_plant(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    form = PlantForm(request.POST or None, request.FILES or None, instance=plant)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Plant updated successfully.')
        return redirect('plants:plant_detail', plant_id=plant.id)
    return render(request, 'plants/plant_form.html', {'form': form, 'title': 'Update Plant'})


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == 'POST':
        plant.delete()
        messages.success(request, 'Plant deleted.')
        return redirect('plants:all_plants')
    return render(request, 'plants/plant_confirm_delete.html', {'plant': plant})


def search_plants(request):
    query = request.GET.get('q', '').strip()
    plants = Plant.objects.none()
    if query:
        plants = Plant.objects.filter(name__icontains=query)
    return render(request, 'plants/search.html', {'plants': plants, 'query': query})
