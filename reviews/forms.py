from django import forms


from .models import Review, Ticket


def fields_attribute(fields, label_fields):
    """Modifications d'attributs des champs des formulaires."""
    for idx, field in enumerate(fields):
        fields[field].widget.attrs.update(
            {"class": "fields-margin"})
        fields[field].label = label_fields[idx]


class TicketForm(forms.ModelForm):
    """Formulaire pour les tickets."""
    label_fields = ["Titre", "Description", "Image"]

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields, self.label_fields)


class ReviewForm(forms.ModelForm):
    """Formulaire pour les reviews."""
    label_fields = ["Titre", "Note", "Commentaire"]

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields, self.label_fields)
