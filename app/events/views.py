# views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm 

class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'  # Template for listing events
    context_object_name = 'events'

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'create_event.html'  # Template for creating a new event
    success_url = reverse_lazy('event_list')



