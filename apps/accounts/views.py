from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.core.paginator import Paginator

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {
        "form": form,
    })


@login_required
def profile_view(request):
    plants = request.user.plants.order_by("-created_at")
    paginator = Paginator(plants, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    comments = request.user.plant_comments.select_related("plant").order_by("-created_at")

    return render(request, "accounts/profile.html", {"plants": page_obj, "page_obj": page_obj, "comments": comments})
