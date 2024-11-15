from django.db import models
from django.contrib.auth.models import User
from app.events.models import Event

class EventMember(models.Model):
    ROLE_CHOICES = [
        ('organizer', 'Organizer'),
        ('participant', 'Participant'),
        ('volunteer', 'Volunteer')
    ]
    
    STATUS_CHOICES = [
        ('joined', 'Joined'),
        ('completed', 'Completed'),
        ('absent', 'Absent')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='joined')

    def __str__(self):
        return f"{self.user.username} - {self.event.name} ({self.role})"
