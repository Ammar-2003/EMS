from django.urls import path
from .views import EventMemberView, JoinEventListView, EventWishListView

urlpatterns = [
    path('', EventMemberView.as_view(), name='member'),
    path('join_event_list/', JoinEventListView.as_view(), name='join_event_list'),
    path('event_wish_list/', EventWishListView.as_view(), name='event_wish_list'),
]
