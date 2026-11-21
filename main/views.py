"""Views of the main app: home page, contact us, and the messages from users."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from main.forms import ContactForm
from main.models import Contact
from plants.models import Plant


def home(request: HttpRequest) -> HttpResponse:
    """The newest 3 plants. "More" opens all of them (/plants/all/)."""
    plants = Plant.objects.all().order_by("-created_at")[:3]
    return render(request, "main/home.html", {"plants": plants})


def contact(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:contact_messages")
    else:
        form = ContactForm()
    return render(request, "main/contact.html", {"form": form})


def contact_messages(request: HttpRequest) -> HttpResponse:
    contacts = Contact.objects.all().order_by("-created_at")
    return render(request, "main/contact_messages.html", {"contacts": contacts})
