from django.contrib import admin
from .models import Ticket, Review


# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "id")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "headline", "ticket", "rating", "id")

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
