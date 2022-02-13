from django.contrib import admin
from .models import UserFollows

# Register your models here.
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")


admin.site.register(UserFollows, UserFollowsAdmin)
