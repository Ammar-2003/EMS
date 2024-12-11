from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from app.events.models import Event
from app.tickets.models import CreateTicket
from datetime import datetime, timedelta
import json


class HomeEventListView(ListView):
    model = Event
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_tickets = CreateTicket.objects.select_related('event')

        # Tickets Data
        tickets_data = []
        for ticket in all_tickets:
            # Calculate tickets_sold and total_revenue using methods
            tickets_sold = ticket.tickets_sold()  # Call the method to get tickets sold
            total_revenue = ticket.total_revenue()  # Call the method to get total revenue

            # Convert Decimal values to float for serialization
            tickets_data.append({
                'event_name': ticket.event.name,
                'tickets_sold': tickets_sold,
                'tickets_available': ticket.tickets_available,
                'total_revenue': float(total_revenue),  # Convert Decimal to float
            })

        # Revenue Data
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)
        year_start = today.replace(month=1, day=1)

        # Weekly Revenue Calculation
        weekly_revenue = 0
        for ticket in all_tickets.filter(created_at__gte=week_start):
            weekly_revenue += ticket.total_revenue()  # Calculate revenue for the ticket using the method

        # Monthly Revenue Calculation
        monthly_revenue = 0
        for ticket in all_tickets.filter(created_at__gte=month_start):
            monthly_revenue += ticket.total_revenue()  # Calculate revenue for the ticket using the method

        # Yearly Revenue Calculation
        yearly_revenue = 0
        for ticket in all_tickets.filter(created_at__gte=year_start):
            yearly_revenue += ticket.total_revenue()  # Calculate revenue for the ticket using the method

        # Convert Decimal to float for revenue data
        context['tickets_data'] = tickets_data
        context['revenue_data'] = {
            'weekly': float(weekly_revenue),  # Convert Decimal to float
            'monthly': float(monthly_revenue),  # Convert Decimal to float
            'yearly': float(yearly_revenue),  # Convert Decimal to float
        }
        return context

# New API endpoint to provide data as JSON
def get_tickets_and_revenue(request):
    all_tickets = CreateTicket.objects.select_related('event')

    # Tickets Data
    tickets_data = []
    for ticket in all_tickets:
        tickets_sold = ticket.tickets_sold()
        total_revenue = ticket.total_revenue()

        tickets_data.append({
            'event_name': ticket.event.name,
            'tickets_sold': tickets_sold,
            'tickets_available': ticket.tickets_available,
            'total_revenue': float(total_revenue),  # Convert Decimal to float
        })

    # Revenue Data
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    weekly_revenue = sum(ticket.total_revenue() for ticket in all_tickets.filter(created_at__gte=week_start))
    monthly_revenue = sum(ticket.total_revenue() for ticket in all_tickets.filter(created_at__gte=month_start))
    yearly_revenue = sum(ticket.total_revenue() for ticket in all_tickets.filter(created_at__gte=year_start))

    # Prepare JSON response
    response_data = {
        'ticketsData': tickets_data,
        'revenueData': {
            'weekly': float(weekly_revenue),
            'monthly': float(monthly_revenue),
            'yearly': float(yearly_revenue),
        }
    }

    return JsonResponse(response_data)