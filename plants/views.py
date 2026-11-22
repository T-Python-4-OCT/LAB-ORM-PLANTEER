from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Plant
from .forms import PlantForm, CommentForm

def listing(request):
    plants = Plant.objects.all()
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    edible = request.GET.get('is_edible', '')
    if q:
        plants = plants.filter(Q(name__icontains=q) | Q(scientific_name__icontains=q) | Q(about__icontains=q))
    if category:
        plants = plants.filter(category=category)
    if edible in ('true', 'false'):
        plants = plants.filter(is_edible=edible == 'true')
    return render(request, 'plants/list.html', {'plants': plants, 'categories': Plant.Category.choices, 'q': q, 'category': category, 'edible': edible, 'is_search': request.resolver_match.url_name == 'plant_search'})

def detail(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.plant = plant
        comment.save()
        messages.success(request, 'Your growing wisdom has been added.')
        return redirect(plant.get_absolute_url() + '#conversation')
    related = Plant.objects.filter(category=plant.category).exclude(pk=plant.pk)[:3]
    return render(request, 'plants/detail.html', {'plant': plant, 'form': form, 'related': related})

def edit(request, plant_id=None):
    plant = get_object_or_404(Plant, pk=plant_id) if plant_id else None
    form = PlantForm(request.POST or None, request.FILES or None, instance=plant)
    if request.method == 'POST' and form.is_valid():
        plant = form.save()
        messages.success(request, 'Your plant has been saved. Let it grow!')
        return redirect(plant)
    return render(request, 'plants/form.html', {'form': form, 'plant': plant})

def delete(request, plant_id):
    plant = get_object_or_404(Plant, pk=plant_id)
    if request.method == 'POST':
        plant.delete()
        messages.success(request, 'Plant removed from the collection.')
        return redirect('plant_list')
    return render(request, 'plants/delete.html', {'plant': plant})
