from django.shortcuts import render
from app.events.models import Event
from app.categories.models import Category
from app.users.models import EventUser

def global_search(request):
    query = request.GET.get('q', '')  # Get the search query from URL parameters
    event_results = []
    member_results = []
    category_results = []

    if query:
        # Search for events based on different fields
        event_results = Event.objects.filter(
            name__icontains=query  # Search in event name
        ) | Event.objects.filter(
            location__icontains=query  # Search in event location
        ) | Event.objects.filter(
            speaker_name__icontains=query  # Search in speaker name
        ) | Event.objects.filter(
            category__name__icontains=query  # Search in category name
        )

        # Additionally, search for event members (attendees, organizers, etc.)
        member_results = EventUser.objects.filter(
            user__username__icontains=query  # Search member's username
        ) | EventUser.objects.filter(
            role__icontains=query  # Search member's role
        ) | EventUser.objects.filter(
            phone_number__icontains=query  # Search member's phone number
        )
        
        # Search for categories
        category_results = Category.objects.filter(
            name__icontains=query  # Search category name
        )
        
    return render(request, 'search_results.html', {
        'query': query,
        'event_results': event_results,
        'member_results': member_results,
        'category_results': category_results
    })
