from django.shortcuts import render, redirect
from .models import Contact
from Plants.models import Plant

# Create your views here.
def home(request):
    plants = Plant.objects.all().order_by("-created_at")

    return render(request, "Main/home.html", {
        "plants": plants
    })


def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            email=request.POST.get("email"),
            message=request.POST.get("message")
        )

        return redirect("contact")

    return render(request, "Main/contact.html")


def contact_messages(request):
    messages = Contact.objects.all().order_by("-created_at")

    return render(request, "Main/contact_messages.html", {
        "messages": messages
    })

