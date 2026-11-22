from django.shortcuts import render
from plants.models import Plant
from .forms import ContactForm
from .models import Contact

def home(request):
    plants = Plant.objects.all()[:3]
    return render(request, "main/home.html", {"plants": plants, "plant_count": Plant.objects.count()})

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return render(request, "main/contact.html", {"form": ContactForm(), "sent": True})
    return render(request, "main/contact.html", {"form": form})

def contact_messages(request):
    return render(request, "main/contact_messages.html", {"contacts": Contact.objects.all()})
