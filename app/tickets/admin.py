from django.contrib import admin
from .models import CreateTicket, Ticket

# Register models
admin.site.register(Ticket)
@admin.register(CreateTicket)
class CreateTicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'price', 'created_at')
    list_filter = ('event__status',)
    search_fields = ('event__name',)
