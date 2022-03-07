from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from django.urls import path


from .views import follow_user, follow_unsubscribe, \
    PasswordChangeViewOverride, signup


urlpatterns = [
    path("signup/", signup, name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_change/",
         PasswordChangeViewOverride.as_view(), name="password-change"),
    path("password_change_done",
         PasswordChangeDoneView.as_view(
             template_name="authentication/password_change_done.html"),
         name="password_change_done"),
    path("follow/", follow_user, name="follow-user"),
    path("follow/<int:relation_id>/<str:follower_name>/unsubscribe/",
         follow_unsubscribe, name="follow-unsubscribe"),
]
