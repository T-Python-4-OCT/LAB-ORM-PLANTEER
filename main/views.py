from django.shortcuts import redirect, render
from .forms import ContactForm
# Create your views here.
from plants.models import Plant
from django.contrib import messages


def home(request):
    plants = Plant.objects.order_by("-created_at")[:3]

    return render(request, "main/home.html", {
        "plants": plants
    })
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})