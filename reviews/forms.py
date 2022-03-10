from django import forms


from .models import Review, Ticket


RATINGS = [
    ('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
]


def fields_attribute(fields, label_fields):
    """Modifications d'attributs des champs d'un formulaire."""
    for idx, field in enumerate(fields):
        fields[field].widget.attrs.update({"class": "fields-margin"})
        fields[field].label = label_fields[idx]
        if fields[field].label == "Note":
            fields[field].widget.attrs.update(
                {"class": "fields-margin rating-tag"}
            )


class TicketForm(forms.ModelForm):
    """Formulaire pour les tickets."""
    label_fields = ["Titre", "Description", "Image"]

    class Meta:
        """Paramètres du formulaire."""
        model = Ticket
        fields = ["title", "description", "image"]
        # widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        """Initialisation du formulaire."""
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields, self.label_fields)


class ReviewForm(forms.ModelForm):
    """Formulaire pour les reviews."""
    label_fields = ["Titre", "Note", "Commentaire"]

    class Meta:
        """Paramètres du formulaire."""
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {"rating": forms.RadioSelect(choices=RATINGS)}

    def __init__(self, *args, **kwargs):
        """Initialisation du formulaire."""
        super().__init__(*args, **kwargs)
        fields_attribute(self.fields, self.label_fields)
