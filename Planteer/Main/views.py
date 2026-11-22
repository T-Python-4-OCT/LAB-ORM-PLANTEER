from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "Main/home.html")

def contact(request):
    return render(request, "Main/contact.html")

def contact_messages(request):
    return render(request, "Main/contact_messages.html")
