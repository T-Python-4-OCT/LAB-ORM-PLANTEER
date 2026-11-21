from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant, Comment


# All Plants
def all_plants(request):

    plants = Plant.objects.all().order_by('-created_at')

    category = request.GET.get('category', '')
    is_edible = request.GET.get('is_edible', '')

    if category:
        plants = plants.filter(category=category)

    if is_edible == 'True':
        plants = plants.filter(is_edible=True)

    elif is_edible == 'False':
        plants = plants.filter(is_edible=False)

    return render(request, 'plants/all_plants.html', {
        'plants': plants,
        'categories': Plant.Category.choices,
        'category': category,
        'is_edible': is_edible
    })


# Add New Plant
def add_plant(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        about = request.POST.get('about')
        used_for = request.POST.get('used_for')
        category = request.POST.get('category')
        is_edible = request.POST.get('is_edible') == 'True'
        image = request.FILES.get('image')

        if name and about and used_for and image and category in Plant.Category.values:

            new_plant = Plant(
                name=name,
                about=about,
                used_for=used_for,
                category=category,
                is_edible=is_edible,
                image=image
            )

            new_plant.save()

            return redirect('all_plants')

    return render(request, 'plants/add_plant.html', {
        'categories': Plant.Category.choices
    })


# Plant Details
def plant_detail(request, plant_id):

    plant = get_object_or_404(Plant, id=plant_id)

    related_plants = Plant.objects.filter(
        category=plant.category
    ).exclude(id=plant.id).order_by('-created_at')[:3]

    comments = plant.comment_set.all().order_by('-created_at')

    return render(request, 'plants/plant_detail.html', {
        'plant': plant,
        'related_plants': related_plants,
        'comments': comments
    })


# Update Plant
def update_plant(request, plant_id):

    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':

        name = request.POST.get('name')
        about = request.POST.get('about')
        used_for = request.POST.get('used_for')
        category = request.POST.get('category')

        if name and about and used_for and category in Plant.Category.values:

            plant.name = name
            plant.about = about
            plant.used_for = used_for
            plant.category = category
            plant.is_edible = request.POST.get('is_edible') == 'True'

            image = request.FILES.get('image')

            if image:
                plant.image = image

            plant.save()

            return redirect('plant_detail', plant_id=plant.id)

    return render(request, 'plants/update_plant.html', {
        'plant': plant,
        'categories': Plant.Category.choices
    })


# Delete Plant
def delete_plant(request, plant_id):

    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':

        plant.delete()

        return redirect('all_plants')

    return redirect('plant_detail', plant_id=plant.id)


# Search Plants
def search_plant(request):

    search = request.GET.get('search', '').strip()

    if search:

        plants = Plant.objects.filter(
            name__icontains=search
        ).order_by('-created_at')

    else:
        plants = []

    return render(request, 'plants/search.html', {
        'plants': plants,
        'search': search
    })


# Add Comment
def add_comment(request, plant_id):

    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':

        full_name = request.POST.get('full_name', '').strip()
        content = request.POST.get('content', '').strip()

        if full_name and content and len(full_name) <= 200:

            new_comment = Comment(
                plant=plant,
                full_name=full_name,
                content=content
            )

            new_comment.save()

    return redirect('plant_detail', plant_id=plant.id)