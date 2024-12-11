from django.db import models
from django.contrib.auth.models import User
from app.events.models import Event

class EventWishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s wish list - {self.event.name}"
