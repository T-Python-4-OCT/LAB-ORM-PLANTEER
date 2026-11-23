from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect, render

from plants.models import Plant

from .forms import ContactForm
from .models import Contact


def home_view(request):
    # Show the 3 newest plants (the model's Meta.ordering is newest first)
    latest_plants = Plant.objects.all()[:3]

    # Count plants in each category with ONE database query (GROUP BY category):
    # values_list("category") groups the rows, annotate(Count) counts each group.
    # order_by() clears Meta.ordering so it doesn't break the grouping.
    counts = dict(
        Plant.objects.values_list("category").annotate(total=Count("id")).order_by()
    )

    # Keep the order of Category.choices and hide empty categories
    categories = [
        {"value": value, "label": label, "count": counts[value]}
        for value, label in Plant.Category.choices
        if value in counts
    ]

    return render(request, "main/home.html", {"plants": latest_plants, "categories": categories})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out! We received your message.")
            return redirect("main:contact")
    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})


def contact_messages_view(request):
    contact_messages = Contact.objects.all()
    return render(request, "main/contact_messages.html", {"contact_messages": contact_messages})
