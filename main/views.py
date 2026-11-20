from django.contrib import messages
from django.shortcuts import redirect, render
from plants.models import Plant
from .forms import ContactForm
from .models import Contact


def home(request):
    return render(request, 'main/home.html', {'plants': Plant.objects.all()[:3]})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Thank you! Your message was sent.')
        return redirect('main:contact')
    return render(request, 'main/contact.html', {'form': form})


def contact_messages(request):
    return render(request, 'main/contact_messages.html', {'contacts': Contact.objects.all()})
