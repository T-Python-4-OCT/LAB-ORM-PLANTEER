
from django.shortcuts import render, redirect

from .models import Contact
from .forms import ContactForm


def contact_home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("contact:home")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})


def contact_messages(request):
    messages = Contact.objects.order_by("-created_at", "-id")

    return render(
        request,
        "contact/messages.html",
        {"contact_messages": messages}
    )
