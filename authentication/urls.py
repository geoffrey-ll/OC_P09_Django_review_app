from django.urls import path
from django.contrib.auth.views import LoginView     # A AJOUTER
from django.contrib.auth.views import LogoutView   # A AJOUTER
from django.contrib.auth.views import PasswordChangeView    # A AJOUTER
from django.contrib.auth.views import PasswordChangeDoneView    # A AJOUTER
from django.conf import settings


from .views import signup
# from .views import login_view
# from .views import logout_view


urlpatterns = [
    path("signup/", signup, name="signup"),
    # path("login/", login_view, name="login"),
    # path("logout/", logout_view, name="logout"),
    path("login/", LoginView.as_view(
        template_name="authentication/login.html",
        redirect_authenticated_user=True), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_change/", PasswordChangeView.as_view(
        template_name="authentication/password_change.html",
    ), name="password-change"),
    path("password_change_done", PasswordChangeDoneView.as_view(
        template_name="authentication/password_change_done.html"
    ), name="password_change_done"),
]
