
from .models import ContactMessage
from django.shortcuts import render, redirect
from plants.models import Plant


def home(request):
    plants = Plant.objects.all().order_by('-created_at')[:3]

    return render(request, 'main/home.html', {
        'plants': plants
    })

def contact(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            return redirect('contact')

    return render(request, 'main/contact.html')

def contact_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')

    return render(request, 'main/messages.html', {
        'messages': messages
    })
