from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Commander(models.Model):
    # relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # commander info
    cmdr_name = models.CharField('commander name', max_length=25, blank=False, null=True)

    # distant worlds 2 info (see roster)
    roster_num = models.PositiveSmallIntegerField('roster number', blank=False, null=True)
    # ...

    def __str__(self):
        return "CMDR {}".format(self.cmdr_name)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Commander.objects.create(user=instance)
    instance.commander.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.commander.save()