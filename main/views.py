from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods, require_safe

from plants.models import Plant

from .forms import ContactForm
from .models import Contact


@require_safe
def home(request):
    return render(request, "main/home.html", {"plants": Plant.objects.all()[:3]})


@require_http_methods(["GET", "POST"])
def contact(request):
    form = ContactForm(request.POST if request.method == "POST" else None)
    if form.is_valid():
        form.save()
        messages.success(request, _("Your message was sent."))
        return redirect("main:contact")
    return render(request, "main/contact.html", {"form": form})


@staff_member_required
@require_safe
def contact_messages(request):
    return render(request, "main/contact_messages.html", {"entries": Contact.objects.all()})
