from django.contrib import admin


from .models import UserFollow


# Register your models here.
class UserFollowsAdmin(admin.ModelAdmin):
    """Colonnes des relations présentes dans l'Admin Django."""
    list_display = ("user", "followed_user")


admin.site.register(UserFollow, UserFollowsAdmin)
