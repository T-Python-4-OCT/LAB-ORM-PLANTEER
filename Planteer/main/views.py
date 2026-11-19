from django.shortcuts import render, redirect
from django.http import HttpRequest
from plants.models import Plant, Comment
from .models import Contact


def home_view(request: HttpRequest):

    plants = Plant.objects.order_by("-created_at")[:3]
    spotlight = Plant.objects.order_by("?").first()
    latest_comments = Comment.objects.order_by("-created_at")[:3]

    categories = []
    for value, label in Plant.Category.choices:
        category_plants = Plant.objects.filter(category=value)
        categories.append({
            "value": value,
            "label": label,
            "count": category_plants.count(),
            "cover": category_plants.first(),
        })

    return render(request, "main/home.html", {
        "plants": plants,
        "spotlight": spotlight,
        "latest_comments": latest_comments,
        "categories": categories,
    })


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
