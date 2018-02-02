import hashlib

from django.db import models
from django.utils.text import slugify

from core.models import Commander


class Location(models.Model):
    # system
    sector = models.CharField(max_length=32, null=True, blank=True)
    subsector = models.CharField(max_length=32, null=True, blank=True)
    system = models.CharField(max_length=128)  # if unique system, put entire system name here

    # body
    body = models.CharField(max_length=32, null=True, blank=True)

    # todo: integrate with edsm? (make another class and link via fk)


class Image(models.Model):

    def user_media_folder(self, filename):
        """return the media folder for a certain user"""
        self.orig_filename = filename
        if self.owner:
            return 'uploads/{}/{}'.format(slugify(self.owner.cmdr_name), filename)  # self.owner.cmdr_name
        else:
            return 'uploads/anonymous/{}'.format(filename)

    # id is automatic

    # utility fields
    sha1sum = models.CharField(unique=True, max_length=40, blank=True)

    # filesystem
    file = models.ImageField(upload_to=user_media_folder)
    orig_filename = models.CharField('original filename', max_length=768, blank=True)
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True)

    # image meta
    desc = models.CharField('description', max_length=768, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    # user
    owner = models.ForeignKey(Commander, on_delete=models.SET_NULL, null=True, blank=True)

    # image uses
    public = models.BooleanField(default=False)
    contest_entry = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk: # if file is new
            sha1 = hashlib.sha1()
            for chunk in self.file.chunks():
                sha1.update(chunk)
            self.sha1sum = sha1.hexdigest()

        super(Image, self).save()

# todo: for upload template, make 'file' and 'url' tabs and use ajax to rewrite the page accordingly

