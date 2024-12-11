from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),  # Event list on event page         
    path('create/', views.EventCreateView.as_view(), name='create_event'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
]
