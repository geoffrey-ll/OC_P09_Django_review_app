from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder_list = \
            ["Nom d'utilisateur", "Mot de passe", "Confirmer mot de passe"]

        for idx, key in enumerate(self.fields):
            self.fields[key].widget.attrs.update(
            {"class": "fields-margin"})
            self.fields[key].widget.attrs.update(
                {"placeholder": f"{placeholder_list[idx]:^60}"})


class LoginForm(AuthenticationForm)  :
    # username = forms.CharField(max_length=150)
    # password = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "fields-margin"})
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Nom d'utilisateur"})
        self.fields["password"].widget.attrs.update(
            {"placeholder": "Mot de passe"})
