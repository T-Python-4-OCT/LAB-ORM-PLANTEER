from django.shortcuts import render, redirect
from plants.models import Plant
from .models import Contact


def home_view(request):
    plants = Plant.objects.order_by("-created_at")[:3]
    return render(request, "main/home.html", {"plants": plants})


def contact_view(request):
    if request.method == "POST":
        Contact.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            message=request.POST["message"],
        )
        return redirect("main:messages")

    return render(request, "main/contact.html")


def messages_view(request):
    contacts = Contact.objects.order_by("-created_at")
    return render(request, "main/messages.html", {"contacts": contacts})