from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from plants.models import Plant
from .models import Contact


def home(request: HttpRequest):
    latest_plants = Plant.objects.all().order_by("-created_at")[:3]
    return render(request, "main/home.html", {"latest_plants": latest_plants})


def contact(request: HttpRequest):
    entry = Contact()
    errors = {}

    if request.method == "POST":
        entry.first_name = request.POST.get("first_name", "").strip()
        entry.last_name = request.POST.get("last_name", "").strip()
        entry.email = request.POST.get("email", "").strip()
        entry.message = request.POST.get("message", "").strip()

        try:
            entry.full_clean()
        except ValidationError as e:
            for field, field_errors in e.message_dict.items():
                errors[field] = field_errors[0]
        else:
            entry.save()
            return redirect("/contact/?sent=1")

    return render(request, "main/contact.html", {
        "entry": entry,
        "errors": errors,
        "sent": request.GET.get("sent") == "1",
    })


def messages(request: HttpRequest):
    entries = Contact.objects.all().order_by("-created_at")
    return render(request, "main/messages.html", {"entries": entries})