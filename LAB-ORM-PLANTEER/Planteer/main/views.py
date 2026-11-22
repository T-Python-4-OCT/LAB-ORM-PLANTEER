from django.shortcuts import render, redirect
from Planteer.plants.models import Plant
from .models import Contact


# Home Page
def home(request):

    plants = Plant.objects.all().order_by('-created_at')[:3]

    return render(request, 'main/home.html', {
        'plants': plants
    })


# Contact Us
def contact(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if first_name and last_name and email and message:

            new_contact = Contact(
                first_name=first_name,
                last_name=last_name,
                email=email,
                message=message
            )

            new_contact.save()

            return redirect('contact')

    return render(request, 'main/contact.html')


# Contact Messages
def contact_messages(request):

    messages = Contact.objects.all().order_by('-created_at')

    return render(request, 'main/messages.html', {
        'messages': messages
    })