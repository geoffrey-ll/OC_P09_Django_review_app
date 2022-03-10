from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image


class Ticket(models.Model):
    """Modèle d'un ticket."""
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2_048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="ticket_images")
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (120, 160)  # (largeur, hauteur)

    def _resize_image(self):
        """Sauvegarde la cover redimentionné."""
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """
        Extension de la sauvegarde de défaut, pour le redimensionnement de
        l'image.
        """
        super().save(*args, **kwargs)
        if self.image:
            self._resize_image()

    def __str__(self):
        """Représentation de la classe."""
        return f"{self.user} : \n" \
               f"{self.title[:50]} : \n" \
               f"{self.description[:30]}"


class Review(models.Model):
    """Modèle d'une review"""
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                          MaxValueValidator(5)]
                                              )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8_192, blank=True)

    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        "Unicité d'une review à un ticket par un user."
        unique_together = ("user", "ticket")

    def __str__(self):
        """Représentation de la classe."""
        return str((self.headline, self.ticket, self.user))
