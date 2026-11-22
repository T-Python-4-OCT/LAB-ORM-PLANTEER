from django.http import HttpRequest
from django.shortcuts import render, redirect
from .models import Contact
from plants.models import Plant


def home_view(request):
    plants = Plant.objects.all().order_by("-created_at")[:3]
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


def contact_messages_view(request):
    contacts = Contact.objects.all().order_by("-created_at")
    return render(request, "main/contact_messages.html", {"contacts": contacts})


def mode_view(request: HttpRequest, mode):

    response = redirect(request.GET.get("next", "/"))

    if mode == "light":
        response.set_cookie("mode", "light", max_age=60 * 60 * 24 * 365)
    elif mode == "dark":
        response.set_cookie("mode", "dark", max_age=60 * 60 * 24 * 365)

    return response 