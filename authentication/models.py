from django.conf import settings
from django.db import models


# Create your models here.
class UserFollow(models.Model):
    """Modèle de la relation d'un utilisateur."""
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="following")
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name="followed_by")

    class Meta:
        """Unicité de la relation."""
        unique_together = ("user", "followed_user")

    def __str__(self):
        """Représentation de la classe."""
        return f"{self.user} & {self.followed_user}"
