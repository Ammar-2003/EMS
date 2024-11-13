from django.db import models
from django.contrib.auth.models import User
from app.events.models import Event

class UserMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    mark = models.IntegerField()
    remarks = models.TextField()

    def __str__(self):
        return f"Mark for {self.user.username} in {self.event.name}"
