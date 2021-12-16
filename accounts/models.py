from django.contrib.auth.models import Group, User
from django.db import models

# Create your models here.
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profiles", on_delete=models.CASCADE)
    bio = models.CharField(max_length=350)

    def __str__(self):
        return self.user.username


@receiver(models.signals.post_save, sender=User)
def post_save_user_signal_handler(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='new_member')
        instance.groups.add(group)
        instance.save()
