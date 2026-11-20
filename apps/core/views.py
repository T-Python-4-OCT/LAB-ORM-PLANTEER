from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.plants.models import Plant
from .models import Contact
from .forms import ContactForm


def home(request):
    plants = Plant.objects.order_by("-created_at")[:6]

    return render(request, "core/home.html", {
        "plants": plants,
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your message has been sent successfully."
            )
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {
        "form": form,
    })


@staff_member_required(login_url="login")
def contact_messages(request):
    contacts = Contact.objects.order_by("-created_at")

    return render(request, "core/contact_messages.html", {
        "contacts": contacts,
    })
