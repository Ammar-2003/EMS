from django.shortcuts import render
from django.views.generic import ListView
from .models import JoinEvent, EventWishList, EventMember
from django.contrib.auth.mixins import LoginRequiredMixin

class EventMemberView(LoginRequiredMixin, ListView):
    model = EventMember
    template_name = 'event_member.html'
    context_object_name = 'members'

class JoinEventListView(LoginRequiredMixin, ListView):
    model = JoinEvent
    template_name = 'join_event_list.html'
    context_object_name = 'joined_events'

    def get_queryset(self):
        return JoinEvent.objects.filter(user=self.request.user)

class EventWishListView(LoginRequiredMixin, ListView):
    model = EventWishList
    template_name = 'event_wish_list.html'
    context_object_name = 'wish_list'

    def get_queryset(self):
        return EventWishList.objects.filter(user=self.request.user)
