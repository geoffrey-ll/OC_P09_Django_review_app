from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View   # a ajouter


from .forms import SignupForm
# from .forms import LoginForm


# Create your views here.
def index(request):
    return render(request, "base.html")


def signup(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Le redirection doit mener vers le flux de l'utilisateur.
            # A modif dès que le flux est en chantier.
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html",
                  context={"form": form})


@login_required
def flux(request,):
    return render(request, "authentication/flux.html")


# class LoginPage(View):  # AJOUTER VIEW
#     form_class = LoginForm
#     template_name = "authentication/login.html"
#
#     def get(self, request):
#         form = self.form_class()
#         message = ''
#         render(request, self.template_name, context={"form": form,
#                                                      "message": message})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = authenticate(username=form.cleaned_data["username"],
#                                 password=form.cleaned_data["password"])
#             if user is not None:
#                 login(request, user)
#                 return redirect(settings.LOGIN_REDIRECT_URL)

# def login_view(request):
#     form = LoginForm()
#     message = ""
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(username=form.cleaned_data["username"],
#                                 password=form.cleaned_data["password"])
#             if user is not None:
#                 login(request, user)
#                 # éventuellement placer un bonjour machin dans page de redirection.
#                 return redirect(settings.LOGIN_REDIRECT_URL)
#             else:
#                 message = no_valid_login()
#     return render(request, "authentication/login.html",
#                   context={"form": form, "message": message})
#
#
# def logout_view(request):
#     logout(request)
#     return redirect(settings.LOGOUT_REDIRECT_URL)
#
#
# def no_valid_login():
#     return "Identifiants invalides."


