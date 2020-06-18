from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profiles", on_delete=models.CASCADE)
    bio = models.CharField(max_length=350)

    def __str__(self):
        return self.user.username
