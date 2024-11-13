from django.db import models
from django.contrib.auth.models import User
from app.events.models import Event

class EventWish(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wish_detail = models.TextField()

    def __str__(self):
        return f"Wish by {self.user.username} for {self.event.name}"
