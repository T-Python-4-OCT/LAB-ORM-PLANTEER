from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import Contact


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for getting in touch!")
            return redirect("main:contact")
    else:
        form = ContactForm()
    return render(request, "main/contact.html", {"form": form})


def contact_messages(request):
    return render(
        request,
        "main/contact_messages.html",
        {"contacts": Contact.objects.all()},
    )
