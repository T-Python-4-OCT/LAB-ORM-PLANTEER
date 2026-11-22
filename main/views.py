from django.contrib import messages
from django.shortcuts import redirect, render
from plants.models import Plant
from .forms import ContactForm
from .models import Contact

def home(request):
    featured = Plant.objects.filter(category=Plant.Category.VEGETABLE)
    if not featured.exists():
        featured = Plant.objects.all()
    return render(request, 'main/home.html', {'plants': featured[:3], 'plant_count': Plant.objects.count()})

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Message received. Thank you for growing with us!')
        return redirect('contact')
    return render(request, 'main/contact.html', {'form': form})

def contact_messages(request):
    return render(request, 'main/messages.html', {'entries': Contact.objects.all()})
