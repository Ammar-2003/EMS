from .models import ContactMessage
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render

def contact_us(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Send the email
        full_message = f"Message from {name} ({email}):\n\n{message}"
        try:
            send_mail(
                subject=subject,
                message=full_message,
                from_email=email,
                recipient_list=[settings.EMAIL_RECEIVER],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'contact.html')
