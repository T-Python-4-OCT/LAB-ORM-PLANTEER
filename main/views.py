from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_safe, require_http_methods

from plants.models import Plant

from .forms import ContactForm
from .models import Contact


@require_safe
def home(request):
    names = ["Common sunflower", "English lavender", "Sweet basil"]
    picks = {plant.name: plant for plant in Plant.objects.filter(name__in=names).order_by("-pk")}
    featured = [picks[name] for name in names if name in picks]
    if len(featured) < 3:
        featured += list(Plant.objects.exclude(pk__in=[plant.pk for plant in featured])
                         .order_by("-created_at", "-pk")[:3 - len(featured)])
    return render(request, "main/home.html", {
        "featured": featured, "categories": Plant.Category.choices,
    })


@require_http_methods(["GET", "HEAD", "POST"])
def contact(request):
    form = ContactForm(request.POST) if request.method == "POST" else ContactForm()
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Thanks for getting in touch. Your message was received.")
        return redirect("main:contact")
    return render(request, "main/contact.html", {"form": form})


@require_safe
def inbox(request):
    return render(request, "main/inbox.html", {"entries": Contact.objects.all()})
