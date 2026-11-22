from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, render

from plants.models import Contact, Plant  # all models live in plants/models.py

from .forms import ContactForm

HOME_PLANTS_LIMIT = 6  # how many of the newest plants the home page shows


def home(request):
    # order_by is needed: Meta.ordering is ignored in queries that use annotate(Count)
    plants = Plant.objects.annotate(comments_count=Count("comments")).order_by("-created_at")[:HOME_PLANTS_LIMIT]
    return render(request, "main/home.html", {
        "plants": plants,
        "plants_count": Plant.objects.count(),
        "categories": Plant.Category.choices,
    })


def contact(request):
    """Contact Us page: empty form (GET) or save the message (POST)."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            entry = form.save()
            messages.success(request, f"Thank you {entry.first_name}! Your message was sent.")
            return redirect("main:contact")
    else:
        form = ContactForm()
    return render(request, "main/contact.html", {"form": form})


def contact_messages(request):
    """All messages sent from the Contact Us page, newest first."""
    return render(request, "main/contact_messages.html", {"entries": Contact.objects.all()})
