from django import forms


from . import models


class TicketForm(forms.ModelForm):

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            # 'class': 'form-input',
            # 'required': '',
            # 'name': 'username',
            # 'id': 'username',
            # 'type': 'text',
            'placeholder': "Titre",
            # 'maxlength': '16',
            # 'minlength': '5',
        })
        self.fields['description'].widget.attrs.update({
            # 'class': 'form-input',
            # 'required': '',
            # 'name': 'password',
            # 'id': 'password',
            # 'type': 'password',
            'placeholder': 'Écrivez une description',
            # 'maxlength': '22',
            # 'minlength': '8'
        })


class ReviewForm(forms.ModelForm):

    class Meta:
        model = models.Review
        fields = ["ticket", "headline", "rating", "body"]
