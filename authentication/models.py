from django.db import models
from django.conf import settings


# Create your models here.
class UserFollow(models.Model):
    """Relation d'un utilisateur."""
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="following")
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name="followed_by")

    class Meta:
        unique_together = ("user", "followed_user")

    def __str__(self):
        return f"{self.user} & {self.followed_user}"
