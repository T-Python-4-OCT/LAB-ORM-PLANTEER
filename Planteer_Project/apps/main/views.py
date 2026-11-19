import random

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from apps.plants.models import Plant

from .forms import ContactForm
from .models import Contact


def home(request):

    categories = list(
        Plant.objects.order_by()
        .values_list("category", flat=True)
        .distinct()
    )

    selected_categories = random.sample(
        categories,
        min(3, len(categories))
    )

    featured_plants = []

    for category in selected_categories:

        plant = Plant.objects.filter(
            category=category
        ).order_by("?").first()

        if plant:
            featured_plants.append(plant)

    context = {
        "featured_plants": featured_plants,
    }

    return render(request, "main/home.html", context)
@require_http_methods(["GET", "POST"])
def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Your message has been submitted successfully."
            )

            return redirect("main:contact")

    else:

        form = ContactForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "main/contact.html",
        context
    )
@require_http_methods(["GET", "POST"])
def contact_messages(request):

    # Handle message actions

    if request.method == "POST":

        action = request.POST.get("action")

        if action not in ["read", "unread", "delete"]:
            return HttpResponseBadRequest("Invalid action.")

        try:
            contact_id = int(request.POST.get("contact_id", ""))
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid message ID.")

        contact_message = get_object_or_404(
            Contact,
            id=contact_id
        )

        if action == "read":

            contact_message.is_read = True
            contact_message.save(update_fields=["is_read"])

            messages.success(
                request,
                "Message marked as read."
            )

        elif action == "unread":

            contact_message.is_read = False
            contact_message.save(update_fields=["is_read"])

            messages.success(
                request,
                "Message marked as unread."
            )

        elif action == "delete":

            contact_message.delete()

            messages.success(
                request,
                "Message deleted successfully."
            )

        url = reverse("main:contact_messages")
        params = request.GET.urlencode()

        return redirect(
            f"{url}?{params}" if params else url
        )


    # Retrieve messages

    contact_list = Contact.objects.all()

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")
    sort = request.GET.get("sort", "newest")


    # Search

    if query:

        contact_list = contact_list.annotate(
            full_name=Concat(
                "first_name",
                Value(" "),
                "last_name"
            )
        ).filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(message__icontains=query)
        )


    # Filter

    if status == "read":

        contact_list = contact_list.filter(
            is_read=True
        )

    elif status == "unread":

        contact_list = contact_list.filter(
            is_read=False
        )

    else:
        status = "all"


    # Sorting

    if sort == "oldest":

        contact_list = contact_list.order_by(
            "created_at", "id"
        )

    else:

        sort = "newest"

        contact_list = contact_list.order_by(
            "-created_at", "-id"
        )


    # Pagination

    paginator = Paginator(contact_list, 10)

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    page_range = paginator.get_elided_page_range(
        page_obj.number,
        on_each_side=2,
        on_ends=1
    )


    # Context

    context = {
        "page_obj": page_obj,
        "page_range": page_range,
        "query": query,
        "status": status,
        "sort": sort,
        "total_messages": paginator.count,
    }

    return render(
        request,
        "main/contact_messages.html",
        context
    )