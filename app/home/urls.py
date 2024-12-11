from django.urls import path
from .views import HomeEventListView
from .import views


urlpatterns = [
    path('', HomeEventListView.as_view(), name='home'),
    path('api/get_tickets_and_revenue/', views.get_tickets_and_revenue, name='get_tickets_and_revenue'),
]
