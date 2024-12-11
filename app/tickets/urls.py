# tickets/urls.py
from django.urls import path
from .views import TicketCreateView
from . import views
urlpatterns = [
    path('', TicketCreateView.as_view(), name='ticket'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),

]
