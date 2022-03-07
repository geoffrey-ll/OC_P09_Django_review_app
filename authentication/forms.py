from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm


PLACEHOLDER_LIST = \
    ["Nom d'utilisateur", "Mot de passe", "Confirmer mot de passe"]


def fields_attribute(fields, option="", placeholder=PLACEHOLDER_LIST):
    """Modifications d'attributs des champs des formulaires."""
    if option == "FollowForm":
        field_class = "size-search-field"
    else:
        field_class = "fields-margin"

    for idx, field in enumerate(fields):
        fields[field].widget.attrs.update(
            {"class": field_class,
             "placeholder": placeholder[idx]})


class SignupForm(UserCreationForm):
    """Formulaire d'inscription."""
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields)


class LoginForm(forms.Form):
    """Formulaire de connexion."""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields)


class FollowForm(forms.Form):
    """Formulaire pour suivre un utilisateur."""
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields, "FollowForm")


class PasswordChangeFormOverride(PasswordChangeForm):
    """Formulaire de changement de mot de passe."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.placeholder_list = []
        for field in self.fields:
            self.placeholder_list.append(self.fields[field].label)
        fields_attribute(self.fields, placeholder=self.placeholder_list)
