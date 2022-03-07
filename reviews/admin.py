from django.contrib import admin


from .models import Review, Ticket


# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    """Colonnes des tickets présentes dans l'Admin Django."""
    list_display = ("user", "id", "title")


class ReviewAdmin(admin.ModelAdmin):
    """Colonnes des reviews présentes dans l'Admin Django."""
    list_display = ("user", "id", "ticket_id", "rating", "headline", "ticket")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
