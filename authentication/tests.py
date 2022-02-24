from django.contrib.auth.models import User
from django.shortcuts import redirect


def user_exist(user):
    try:
        user_to_reset = User.objects.get(username=user)
    except:
        user_to_reset = None
    return user_to_reset
