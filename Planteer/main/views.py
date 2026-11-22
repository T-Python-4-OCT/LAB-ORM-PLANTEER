from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from plants.models import Plant
from .models import Contact


def home_view(request: HttpRequest):

    plants = Plant.objects.order_by("-created_at")[:3]

    return render(request, "main/home.html", {"plants": plants})


def contact_view(request: HttpRequest):

    if request.method == "POST":
        new_contact = Contact(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            message=request.POST["message"],
        )
        new_contact.save()

        return redirect("main:contact_messages_view")

    return render(request, "main/contact.html")


def contact_messages_view(request: HttpRequest):

    contacts = Contact.objects.order_by("-created_at")

    return render(request, "main/contact_messages.html", {"contacts": contacts})


def delete_contact_view(request: HttpRequest, contact_id: int):

    contact = get_object_or_404(Contact, pk=contact_id)

    if request.method == "POST":
        contact.delete()

    return redirect("main:contact_messages_view")
