from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from app.events.models import Event
from app.users.models import EventUser
from django.db.models import Sum


class CreateTicket(models.Model):
    event = models.OneToOneField(
        Event,
        on_delete=models.CASCADE,
        limit_choices_to={'status': 'upcoming'},
        verbose_name="Tickets for Upcoming Events"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price for a single ticket
    tickets_available = models.PositiveIntegerField(default=100)  # Total tickets admin is making available
    created_at = models.DateTimeField(auto_now_add=True)

    def tickets_sold(self):
        """Calculate the total tickets sold."""
        return self.ticket_set.aggregate(total=Sum('quantity'))['total'] or 0

    def total_revenue(self):
        """Calculate the total revenue."""
        return self.tickets_sold() * self.price

    def clean(self):
        """Ensure tickets can only be created for upcoming events."""
        if self.event.status != 'upcoming':
            raise ValidationError("Tickets can only be created for upcoming events.")

    def save(self, *args, **kwargs):
        """Perform validation and save the model."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tickets for {self.event.name} at ${self.price} each"

    def get_absolute_url(self):
        return reverse('create_ticket')


class Ticket(models.Model):
    user = models.ForeignKey(EventUser, on_delete=models.CASCADE)
    available_ticket = models.ForeignKey(
        CreateTicket,
        on_delete=models.CASCADE,
        verbose_name="Tickets for Upcoming Events"
    )
    quantity = models.PositiveIntegerField(default=1)  # Number of tickets purchased
    purchase_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Ensure ticket purchase is valid."""
        # Ensure the event is still upcoming
        if self.available_ticket.event.status != 'upcoming':
            raise ValidationError("Tickets can only be purchased for upcoming events.")
        # Check if there are enough tickets available
        if self.quantity > self.available_ticket.tickets_available:
            raise ValidationError(f"Only {self.available_ticket.tickets_available} tickets are available for this event.")

    def save(self, *args, **kwargs):
        """Validate and save the ticket while updating available tickets."""
        self.clean()
        # Deduct tickets from the available count
        self.available_ticket.tickets_available -= self.quantity
        self.available_ticket.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} Ticket(s) for {self.available_ticket.event.name} by {self.user}"

    def get_absolute_url(self):
        return reverse('ticket')
