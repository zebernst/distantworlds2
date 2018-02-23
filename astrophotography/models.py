import hashlib
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.text import slugify

from core.models import Commander, Location, Waypoint


# todo: make success_url go to the Location form that pre-populates from filename
class Image(LoginRequiredMixin, models.Model):

    def user_media_folder(self, filename):
        """return the media folder for a certain user"""
        self.orig_filename = filename
        if self.owner:
            return 'uploads/{}/{}'.format(slugify(self.owner.cmdr_name), filename)  # self.owner.cmdr_name
        else:
            return 'uploads/anonymous/{}'.format(filename)

    def waypoint_folder(self, filename):
        # save original filename
        self.orig_filename = filename

        # todo: parse filename for system info

        # todo: add cmdr_name to filename

        cmdr = slugify('Anonymous' if self.owner.cmdr_name is None else self.owner.cmdr_name)
        wp = slugify('Misc' if self.waypoint is None else self.waypoint.abbrev)

        return 'uploads/{wp}/{cmdr}_{f}'.format(wp=wp, cmdr=cmdr, f=filename)

    # id is automatic

    # utility fields
    sha1sum = models.CharField(unique=True, max_length=40, blank=True, editable=False)

    # filesystem
    image = models.ImageField(upload_to=waypoint_folder)  # todo: use django-imagekit for processing photos (https://github.com/matthewwithanm/django-imagekit/)
    thumb = models.ImageField(upload_to='thumbs', null=True)

    orig_filename = models.CharField('original filename', max_length=768)
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True)

    # image meta
    desc = models.CharField('description', max_length=768, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    waypoint = models.ForeignKey(Waypoint, on_delete=models.SET_NULL, null=True, blank=False)

    # user
    owner = models.ForeignKey(Commander, on_delete=models.SET_NULL, null=True)

    # image uses
    public = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)

    # imgur
    imgur_url = models.CharField(max_length=512, null=True)
    del_hash = models.CharField(max_length=512, null=True)

    # todo: make flags that indicate whether or not a photo has been "exported"

    def save(self, *args, **kwargs):

        # if file is new, store sha1sum
        # note: important that the sha1sum is calculated BEFORE watermarking images
        if not self.pk:
            sha1 = hashlib.sha1()
            for chunk in self.image.chunks():
                sha1.update(chunk)
            self.sha1sum = sha1.hexdigest()

        # save user

        # convert .bmp files before saving
        name, ext = os.path.splitext(self.image.name)
        if ext.lower() == ".bmp":
            # do conversion
            pass

        # watermark, etc.

        # generate thumbnail
        if not self.thumb:
            # create thumbnail
            pass

        # save image
        super(Image, self).save(*args, **kwargs)


# delete the image file when the Image instance is deleted by the admin panel.
@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    instance.image.delete(False)  # pass False to ensure that a save() isn't called.
    if instance.thumb:
        instance.thumb.delete(False)

# todo: for upload template, make 'file' and 'url' tabs and use ajax to rewrite the page accordingly

