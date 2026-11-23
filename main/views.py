from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, render

from plants.models import Comment, Plant

from .forms import ContactForm
from .models import Contact

CATEGORY_ICONS = {
    'tree': '🌳',
    'fruit': '🍎',
    'vegetable': '🥕',
    'herb': '🌿',
    'flower': '🌸',
    'succulent': '🌵',
}


def home_view(request):
    counts = dict(Plant.objects.values_list('category').annotate(n=Count('id')))
    categories = [
        {'value': value, 'label': label, 'icon': CATEGORY_ICONS.get(value, '🌱'), 'count': counts.get(value, 0)}
        for value, label in Plant.Category.choices
    ]
    return render(request, 'main/home.html', {
        'plants': Plant.objects.all()[:3],
        'categories': categories,
        'stats': {
            'plants': Plant.objects.count(),
            'edible': Plant.objects.filter(is_edible=True).count(),
            'comments': Comment.objects.count(),
        },
    })


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thanks! Your message was sent.')
            return redirect('main:contact')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})


def contact_messages_view(request):
    return render(request, 'main/contact_messages.html', {'contacts': Contact.objects.all()})
