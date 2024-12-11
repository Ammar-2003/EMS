from django.views.generic import ListView, CreateView
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Event
from datetime import datetime
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render

class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    paginate_by = 15  # Default items per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Retrieve filters from GET parameters
        status = self.request.GET.get('status', '').strip()
        name = self.request.GET.get('name', '').strip()
        date_filter = self.request.GET.get('date', '').strip()
        location = self.request.GET.get('location', '').strip()

        # Apply filters dynamically
        if status:
            queryset = queryset.filter(status=status)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if date_filter:
            try:
                parsed_date = datetime.strptime(date_filter, "%Y-%m-%d")
                queryset = queryset.filter(date__date=parsed_date.date())
            except ValueError:
                pass  # Ignore invalid date formats
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    def render_to_response(self, context, **response_kwargs):
    # Check if the request is an AJAX request
      if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
        page_number = self.request.GET.get('page', 1)
        paginator = Paginator(context['events'], self.paginate_by)
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj  # Update context with paginated data

        # Pagination logic to display only 3 page numbers
        page_range = self.get_paginated_page_range(page_obj)
        context['page_range'] = page_range  # Pass the custom page range to the template

        # Render the HTML for the table only (excluding the rest of the page)
        html = render_to_string('events_table.html', context, self.request)
        return JsonResponse({'html': html, 'page': page_obj.number, 'total_pages': paginator.num_pages, 'page_range': page_range})

    # For regular requests, return the full page
      return super().render_to_response(context, **response_kwargs)

    def get_paginated_page_range(self, page_obj):
      current_page = page_obj.number
      total_pages = page_obj.paginator.num_pages

    # Define the range of 3 consecutive pages
      if current_page == 1:
        page_range_start = 1
        page_range_end = min(3, total_pages)
      elif current_page == total_pages:
        page_range_start = max(total_pages - 2, 1)
        page_range_end = total_pages
      else:
        page_range_start = max(current_page - 1, 1)  # Always show 1 before
        page_range_end = min(current_page + 1, total_pages)  # Always show 1 after

    # Ensure we return 3 pages (adjust if it's near start or end)
      if page_range_end - page_range_start < 2:
        if current_page <= total_pages - 3:
            page_range_end += 1
        else:
            page_range_start -= 1

      return list(range(page_range_start, page_range_end + 1))

class EventCreateView(CreateView):
    model = Event
    fields = ['name', 'speaker_name', 'location', 'date', 'description', 'status', 'category']
    template_name = 'create_event.html'
    success_url = reverse_lazy('event_list')

def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_details.html', {'event': event})

