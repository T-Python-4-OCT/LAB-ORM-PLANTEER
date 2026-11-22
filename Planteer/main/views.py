
from django.shortcuts import render, redirect
from plants.models import Plant
from .models import Contact
from .forms import ContactForm


def home(request):
    plants = Plant.objects.filter(
        name__in=['Rose', 'Sunflower', 'Lavender']
    )[:3]

    return render(request, 'main/home.html', {
        'plants': plants
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {
        'form': form
    })


def contact_messages(request):
    messages = Contact.objects.all().order_by('-created_at')

    return render(request, 'main/contact_messages.html', {
        'messages': messages
    })
