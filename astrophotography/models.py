from django.contrib.auth.models import User
from django.db import models


class Commander(models.Model):
    # relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # commander info
    cmdr_name = models.CharField('commander name', max_length=25)

    # distant worlds 2 info (see roster)
    roster_num = models.PositiveSmallIntegerField('roster number')
    # ...


class Location(models.Model):
    # system
    sector = models.CharField(max_length=32, null=True, blank=True)
    subsector = models.CharField(max_length=32, null=True, blank=True)
    system = models.CharField(max_length=128)  # if unique system, put entire system name here

    # body
    body = models.CharField(max_length=32, null=True, blank=True)

    # todo: integrate with edsm?


class Image(models.Model):
    # id is automatic

    # utility fields
    sha1sum = models.CharField(unique=True, max_length=40, blank=True)

    # filesystem
    filename = models.CharField(max_length=128)
    orig_filename = models.CharField('original filename', max_length=768, blank=True)
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True)

    # image meta
    desc = models.CharField('description', max_length=768, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    # user
    owner = models.ForeignKey(Commander, on_delete=models.SET_NULL, null=True, blank=True)


