from django.contrib import admin
from .models import EventMember , JoinEvent , EventWishList
# Register your models here.

admin.site.register(EventMember)
admin.site.register(JoinEvent)
admin.site.register(EventWishList)

