from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, render


from .forms import FollowForm, LoginForm, PasswordChangeFormOverride, SignupForm
from .models import UserFollow


MESSAGE_CANT_SIGNUP_WHEN_LOGGED = "Impossible de s'inscrire en étant connecté."
TAGS_CANT_SIGNUP_WHEN_LOGGED = "alert alert-info bs-perso-message"
MESSAGE_SUCCESS_SIGNUP = "Inscription réussi."
TAGS_SUCCESS_SIGNUP = "alert alert-success bs-perso-message"


# Create your views here
class PasswordChangeViewOverride(PasswordChangeView):
    template_name = "authentication/password_change.html"
    form_class = PasswordChangeFormOverride


def signup(request):
    if request.user.is_authenticated:
        messages.error(request, MESSAGE_CANT_SIGNUP_WHEN_LOGGED,
                       extra_tags=TAGS_CANT_SIGNUP_WHEN_LOGGED)
        return redirect(settings.LOGIN_REDIRECT_URL)
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, MESSAGE_SUCCESS_SIGNUP,
                             extra_tags=TAGS_SUCCESS_SIGNUP)
            return redirect("home-page")
    return render(request, "authentication/signup.html",
                  context={"form": form})


def login_view(request):
    if request.user.is_authenticated is True:
        return redirect("flux-user")
    form = LoginForm()
    message = ''
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print(f"\nJe suis valid\n")
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"])
            print(f"\nuser:\n{user}\n")
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                message = "Nom d'utilisateur ou mot de passe invalide."

    return render(request, "authentication/home_page.html",
                  context={"form": form, "message": message})


@login_required
def follow_user(request):
    # Ceux suivit par l'user
    relations_user = UserFollow.objects\
        .filter(user=request.user).order_by("followed_user__username")
    # Ceux qui suivent l'user
    following_users = UserFollow.objects\
        .filter(followed_user=request.user).order_by("user__username")
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
                    to_follow_user = User.objects.get(username=to_search_user)
                    already_follow = UserFollow.objects.filter(
                        user=request.user,
                        followed_user=to_follow_user
                    )
                    if len(already_follow) != 0:
                        message = "Vous suivez déjà cet utilisateur."
                    else:
                        UserFollow.objects.create(
                            user=request.user,
                            followed_user=to_follow_user
                        )
            except:
                # DoesNoExist & IntegrityError
                message = "Utilisateur inconnu."

    return render(request, "authentication/follow_user.html",
                  context={"relations_user": relations_user,
                           "following_users": following_users,
                           "form": form,
                           "message": message})


@login_required
def follow_unsubscribe(request, relation_id, follower_name):
    follow_unsubscribe = UserFollow.objects.get(id=relation_id)
    if follow_unsubscribe.user == request.user:
        if request.method == "POST":
            follow_unsubscribe.delete()
            return redirect("follow-user")
    else:
        return redirect("follow-user")
    return render(request, "authentication/follow_unsubscribe.html",
                  context={"follower_name": follower_name})
