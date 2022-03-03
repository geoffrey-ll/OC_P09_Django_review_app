from django.contrib import admin
from .models import Ticket, Review


# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    """Colonnes des tickets présentes dans l'Admin Django."""
    list_display = ("user", "title", "id")


class ReviewAdmin(admin.ModelAdmin):
    """Colonnes des reviews présentes dans l'Admin Django."""
    list_display = ("user", "headline", "ticket", "rating", "ticket_id", "id")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
