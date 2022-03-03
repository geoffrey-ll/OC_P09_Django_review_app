from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.db import models
from PIL import Image


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2_048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="ticket_images")
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (120, 160) # (largeur, hauteur)

    def _resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self._resize_image()

    def __str__(self):
        return f"{self.user} a demandé une critique\n" \
               f"{self.title}\n" \
               f"{self.description}"


class Review(models.Model):
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
        unique_together = ("user", "ticket")

    def __str__(self):
        return str((self.headline, self.ticket, self.user))
