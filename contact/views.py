from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse
from .models import Contact


def contact_view(request: HttpRequest):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if first_name and last_name and email and message:
            Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                message=message,
            )
            return redirect(reverse("contact:contact_view") + "?sent=1")

    sent = request.GET.get("sent") == "1"
    return render(request, "contact/contact.html", {"sent": sent})


def messages_view(request: HttpRequest):
    contact_messages = Contact.objects.order_by("-created_at")
    return render(request, "contact/messages.html", {"contact_messages": contact_messages})