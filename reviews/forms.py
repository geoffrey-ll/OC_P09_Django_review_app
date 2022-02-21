from django import forms


from . import models


def fields_attribute(fields, label_fields):
    for idx, field in enumerate(fields):
        fields[field].widget.attrs.update(
            {"class": "fields-margin"})
        fields[field].label = label_fields[idx]


class TicketForm(forms.ModelForm):
    label_fields = ["Titre", "Description", "Image"]

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields, self.label_fields)


class ReviewForm(forms.ModelForm):
    label_fields = ["Titre", "Note", "Commentaire"]

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields, self.label_fields)
