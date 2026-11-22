
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from apps.plants.models import Plant, Comment
from apps.core.models import Contact


User = get_user_model()


# ==========================================
# DASHBOARD OVERVIEW
# ==========================================

@staff_member_required(login_url="login")
def dashboard_home(request):
    stats = {
        "plants": Plant.objects.count(),
        "users": User.objects.count(),
        "comments": Comment.objects.count(),
        "messages": Contact.objects.count(),
    }

    recent_plants = Plant.objects.select_related(
        "created_by"
    ).order_by("-created_at", "-id")[:5]

    recent_messages = Contact.objects.order_by(
        "-created_at", "-id"
    )[:5]

    return render(request, "dashboard/index.html", {
        "stats": stats,
        "recent_plants": recent_plants,
        "recent_messages": recent_messages,
    })


# ==========================================
# MANAGE PLANTS
# ==========================================

@staff_member_required(login_url="login")
def dashboard_plants(request):
    plants = Plant.objects.select_related(
        "created_by"
    ).order_by("-created_at", "-id")

    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    owner = request.GET.get("owner", "").strip()

    if query:
        plants = plants.filter(
            Q(name__icontains=query)
            | Q(about__icontains=query)
            | Q(created_by__username__icontains=query)
        )

    if category in Plant.Category.values:
        plants = plants.filter(category=category)

    if owner.isdigit():
        plants = plants.filter(created_by_id=int(owner))

    paginator = Paginator(plants, 10)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    owners = User.objects.filter(
        plants__isnull=False
    ).distinct().order_by("username")

    return render(request, "dashboard/plants.html", {
        "plants": page_obj,
        "page_obj": page_obj,
        "query": query,
        "selected_category": category,
        "selected_owner": owner,
        "categories": Plant.Category.choices,
        "owners": owners,
        "total_results": paginator.count,
    })


# ==========================================
# MANAGE USERS
# ==========================================

@staff_member_required(login_url="login")
def dashboard_users(request):
    users = User.objects.annotate(
        plants_count=Count("plants", distinct=True)
    ).order_by("-date_joined", "-id")

    query = request.GET.get("q", "").strip()
    role = request.GET.get("role", "").strip()

    if query:
        users = users.filter(
            Q(username__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        )

    if role == "staff":
        users = users.filter(is_staff=True)

    elif role == "regular":
        users = users.filter(is_staff=False)

    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(request, "dashboard/users.html", {
        "users": page_obj,
        "page_obj": page_obj,
        "query": query,
        "selected_role": role,
        "total_results": paginator.count,
    })


# ==========================================
# MANAGE COMMENTS
# ==========================================

@staff_member_required(login_url="login")
def dashboard_comments(request):
    comments = Comment.objects.select_related(
        "user",
        "plant",
    ).order_by("-created_at", "-id")

    query = request.GET.get("q", "").strip()

    if query:
        comments = comments.filter(
            Q(content__icontains=query)
            | Q(user__username__icontains=query)
            | Q(plant__name__icontains=query)
        )

    paginator = Paginator(comments, 10)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(request, "dashboard/comments.html", {
        "comments": page_obj,
        "page_obj": page_obj,
        "query": query,
        "total_results": paginator.count,
    })


@staff_member_required(login_url="login")
@require_POST
def dashboard_comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()

    return redirect("dashboard_comments")


# ==========================================
# MANAGE CONTACT MESSAGES
# ==========================================

@staff_member_required(login_url="login")
def dashboard_messages(request):
    contacts = Contact.objects.order_by(
        "-created_at", "-id"
    )

    query = request.GET.get("q", "").strip()

    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(message__icontains=query)
        )

    paginator = Paginator(contacts, 10)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(request, "dashboard/messages.html", {
        "contacts": page_obj,
        "page_obj": page_obj,
        "query": query,
        "total_results": paginator.count,
    })


@staff_member_required(login_url="login")
@require_POST
def dashboard_message_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()

    return redirect("dashboard_messages")
