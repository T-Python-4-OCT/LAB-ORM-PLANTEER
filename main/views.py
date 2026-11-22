from django.http import HttpRequest
from django.shortcuts import redirect, render

from plants.models import Plant

from .forms import ContactForm
from .models import Contact


def home_view(request: HttpRequest):
    # Latest 3 plants only
    plants = Plant.objects.all()[0:3]
    return render(request, "main/index.html", {"plants": plants})


def contact_view(request: HttpRequest):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:contact_messages_view")
    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})


def contact_messages_view(request: HttpRequest):
    return render(request, "main/contact_messages.html", {"messages_list": Contact.objects.all()})
