from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Event

class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    paginate_by = 30

    def get_queryset(self):
        # Get the 'status' and 'name' values from the URL query parameters
        status = self.request.GET.get('status', '').strip()  # If no status, it will be an empty string
        name = self.request.GET.get('name', '').strip()  # Strip any unwanted spaces from the name search
        
        # Start with all events
        events = Event.objects.all()

        # If a valid status is provided, filter events by that status
        if status:
            events = events.filter(status=status)

        # If a valid name is provided, filter events by that name (case-insensitive search)
        if name:
            events = events.filter(name__icontains=name)

        return events

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add the selected status and name to the context to retain the filter in the form
        context['status'] = self.request.GET.get('status', '')
        context['name'] = self.request.GET.get('name', '')
        
        return context
class EventCreateView(CreateView):
    model = Event
    fields = ['name', 'speaker_name', 'location', 'date', 'description', 'status', 'category']
    template_name = 'create_event.html'
    success_url = reverse_lazy('event_list')
