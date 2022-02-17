from django import forms


from . import models


class TicketForm(forms.ModelForm):

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['title'].widget.attrs.update({
    #
    #         "placeholder": "Titre"})
    #
    #     self.fields['description'].widget.attrs.update({
    #         "placeholder": 'Écrivez une description'})


class ReviewForm(forms.ModelForm):

    class Meta:
        model = models.Review
        fields = ["ticket", "headline", "rating", "body"]
