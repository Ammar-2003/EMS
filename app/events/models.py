from django.db import models
from django.urls import reverse
from app.categories.models import Category

class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    speaker_name = models.CharField(max_length=40 , verbose_name='Speaker Name')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')

    def get_absolute_url(self):
        return reverse('event_list')

    def __str__(self):
        return self.name
