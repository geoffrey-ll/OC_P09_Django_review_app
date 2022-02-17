from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View   # a ajouter


from .forms import SignupForm
from .forms import LoginForm
from . import models


# Create your views here.
def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Le redirection doit mener vers le flux de l'utilisateur.
            # A modif dès que le flux est en chantier.
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html",
                  context={"form": form})


def login_view(request):
    form = LoginForm(request)
    print("\nJE SUIS LÀ\n", form)
    if request.method == "POST":
        form = LoginForm(request.POST)
        print("\nJE PASSE EN 2\n", form)
        if form.is_valid():
            print("\nJE PASSE EN 3\n", form, "\n")
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, "authentication/login.html", context={"form": form})



@login_required
def follow_user(request):
    # Ceux suivit par l'user
    relations_user = \
        models.UserFollows.objects.filter(Q(user=request.user))
    # Ceux qui suivent l'user
    following_users = \
        models.UserFollows.objects.filter(Q(followed_user=request.user))

    return render(request, "authentication/follow_user.html",
                  context={"relations_user": relations_user,
                           "following_users": following_users})


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

