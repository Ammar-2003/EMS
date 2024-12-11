from django.urls import path
from .views import home
from .views import HomeEventListView


urlpatterns = [
    path('', HomeEventListView.as_view(), name='home'), # Event list on home page
]
