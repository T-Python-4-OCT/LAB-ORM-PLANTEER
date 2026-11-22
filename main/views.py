from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from plants.models import Plant

from .forms import ContactForm
from .models import Contact


def home_view(request: HttpRequest):
    plants = Plant.objects.order_by("-created_at")[:3]
    return render(request, "main/home.html", {"plants": plants})


def contact_view(request: HttpRequest):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("main:contact_view") + "?sent=1")
    else:
        form = ContactForm()

    context = {"form": form, "sent": request.GET.get("sent") == "1"}
    return render(request, "main/contact.html", context)


def contact_messages_view(request: HttpRequest):
    contact_messages = Contact.objects.order_by("-created_at")
    return render(request, "main/messages.html", {"contact_messages": contact_messages})
