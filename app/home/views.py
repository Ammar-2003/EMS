from django.shortcuts import render
from django.views.generic import ListView
from app.events.models import Event

def home(request):
    return render(request, 'home.html')  # Make sure 'home.html' is in quotes

from itertools import chain

class HomeEventListView(ListView):
    model = Event
    template_name = 'home.html'  # New template for the home page events section
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch limited events by status
        upcoming_events = Event.objects.filter(status='upcoming').order_by('date')[:3]
        completed_events = Event.objects.filter(status='completed').order_by('date')[:3]
        canceled_events = Event.objects.filter(status='cancelled').order_by('date')[:3]
        
        # Combine and sort all events by date
        all_events = sorted(
            chain(upcoming_events, completed_events, canceled_events),
            key=lambda event: event.date
        )
        
        context['all_events'] = all_events  # Pass combined and sorted events
        
        return context
