from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Ticket, CreateTicket
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from app.events.models import Event
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from .models import CreateTicket


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['available_ticket', 'quantity']  # Change 'event' to 'available_ticket' for CreateTicket
    template_name = 'tickets.html'
    success_url = reverse_lazy('ticket')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # Add CSS classes for styling
        form.fields['available_ticket'].widget.attrs.update({'class': 'form-control'})
        form.fields['quantity'].widget.attrs.update({'class': 'form-control', 'min': 1, 'placeholder': 'Enter quantity'})

        # Filter only tickets created for upcoming events
        form.fields['available_ticket'].queryset = CreateTicket.objects.filter(event__status='upcoming')
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user.profile  # Attach the logged-in user (EventUser profile)
        try:
            # Ensure there are enough tickets available
            available_ticket = form.instance.available_ticket
            if form.instance.quantity > available_ticket.tickets_available:
                form.add_error('quantity', f"Only {available_ticket.tickets_available} tickets are available for this event.")
                return self.form_invalid(form)

            # Attempt to clean and save the form (will validate ticket availability, etc.)
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e.message)
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your ticket purchase. Please check your input.")
        return super().form_invalid(form)

# Check if the user is admin
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def create_ticket(request):
    if request.method == "POST":
        event = request.POST.get('event')
        price = request.POST.get('price')
        tickets_available = request.POST.get('tickets_available')

        # Form validation
        if not event or not price or not tickets_available:
            messages.error(request, "All fields are required.")
            return render(request, 'create_ticket.html')

        try:
            # Assuming 'event' is an Event ID; replace with actual Event object
            event_instance = Event.objects.get(id=event)

            # Ensure the event is upcoming
            if event_instance.status != 'upcoming':
                messages.error(request, "Tickets can only be created for upcoming events.")
                return render(request, 'create_ticket.html')

            # Save the new ticket
            new_ticket = CreateTicket(
                event=event_instance,
                price=price,
                tickets_available=tickets_available
            )
            new_ticket.save()

            messages.success(request, "Ticket created successfully!")
            return redirect('ticket')  # Redirect to a ticket list or another page

        except Event.DoesNotExist:
            messages.error(request, "Event not found.")
            return render(request, 'create_ticket.html')
    else:
        # Handle GET request
        events = Event.objects.filter(status='upcoming')
        return render(request, 'create_ticket.html', {'events': events})