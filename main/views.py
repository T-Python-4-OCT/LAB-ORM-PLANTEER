from django.shortcuts import render
from django.http import HttpRequest


def home(request: HttpRequest):
    return render(request, "main/home.html")


def contact(request: HttpRequest):
    return render(request, "main/contact.html")


def messages(request: HttpRequest):
    return render(request, "main/messages.html")