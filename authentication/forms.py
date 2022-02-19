from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm


PLACEHOLDER_LIST = \
    ["Nom d'utilisateur", "Mot de passe", "Confirmer mot de passe"]


class PasswordResetFormOverride(PasswordResetForm):
    user = forms.CharField()


def fields_attribute(fields, option=""):
    if option == "FollowForm":
        field_class = "size-search-field"
    else:
        field_class = "fields-margin"

    for idx, field in enumerate(fields):
        fields[field].widget.attrs.update(
            {"class": field_class,
             "placeholder": PLACEHOLDER_LIST[idx]})


class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields)


class LoginForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields)

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class FollowForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields, "FollowForm")

    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
