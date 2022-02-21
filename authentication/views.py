from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View   # a ajouter
from django.contrib.auth.views import PasswordResetView


from .forms import SignupForm
from .forms import LoginForm
from . import models
from .forms import FollowForm

from .forms import PasswordResetFormOverride


# Create your views here
class PasswordResetViewOverride(PasswordResetView):
    template_name = "authentication/password_change.html"
    form_class = PasswordResetFormOverride




def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            # Le redirection doit mener vers le flux de l'utilisateur.
            # A modif dès que le flux est en chantier.
            return redirect('login')
    return render(request, "authentication/signup.html",
                  context={"form": form})


def login_view(request):
    if request.user.is_authenticated == True:
        return redirect("flux")
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"])
            print(f"\nJe suis user authentifier {user}\n")
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "authentication/login.html", context={"form": form})


@login_required
def follow_user(request):
    # Ceux suivit par l'user
    relations_user = \
        models.UserFollows.objects.filter(Q(user=request.user))\
            .order_by("followed_user__username")
    # Ceux qui suivent l'user
    following_users = \
        models.UserFollows.objects.filter(Q(followed_user=request.user))\
            .order_by("user__username")
    form = FollowForm()
    message = ''

    if request.method == "POST":
        form = FollowForm(request.POST)
        if form.is_valid():
            try:
                to_search_user = form.cleaned_data["username"]
                if to_search_user == str(request.user):
                    message = "Impossible de s'abonner à soi-même."
                else:
                    to_follow_user = \
                        User.objects.get(username=to_search_user)
                    models.UserFollows.objects.create(
                        user=request.user, followed_user=to_follow_user)
            except:
                message = "Utilisateur inconnu."

    return render(request, "authentication/follow_user.html",
                  context={"relations_user": relations_user,
                           "following_users": following_users,
                           "form": form,
                           "message": message})


@login_required
def follow_unsubscribe(request, relation_id, follower_name):
    follow_unsubscribe = models.UserFollows.objects.get(id=relation_id)
    if follow_unsubscribe.user == request.user:
        if request.method == "POST":
            follow_unsubscribe.delete()
            return redirect("follow-user")
    else:
        return redirect("follow-user")
    return render(request, "authentication/follow_unsubscribe.html",
                  context={"follower_name": follower_name})
