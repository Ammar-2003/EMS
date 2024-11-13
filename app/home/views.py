from django.shortcuts import render
from django.views.generic import ListView
from app.events.models import Event

def home(request):
    return render(request, 'home.html')  # Make sure 'home.html' is in quotes

class HomeEventListView(ListView):
    model = Event
    template_name = 'home.html'  # New template for the home page events section
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch 3 upcoming events
        context['upcoming_events'] = Event.objects.filter(status='upcoming').order_by('date')[:3]
        
        # Fetch 2 completed events
        context['completed_events'] = Event.objects.filter(status='completed').order_by('date')[:2]
        
        # Fetch 2 canceled events
        context['canceled_events'] = Event.objects.filter(status='cancelled').order_by('date')[:2]
        
        return context