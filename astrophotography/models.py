import hashlib
import io
from pathlib import Path

from PIL import Image as PImage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.text import slugify
from sorl.thumbnail import delete, ImageField

from core.models import Commander, Location, Waypoint
from distantworlds2.settings.base import SITE_ROOT


class Image(LoginRequiredMixin, models.Model):

    def waypoint_folder(self, filename):
        # save original filename
        self.orig_filename = filename

        # todo: parse filename for system info

        cmdr = slugify('Anonymous' if self.owner.cmdr_name is None else self.owner.cmdr_name)
        wp = slugify('Misc' if self.waypoint is None else self.waypoint.abbrev)
        ext = Path(filename).suffix

        return 'uploads/{wp}/{cmdr}_{hash}{ext}'.format(wp=wp, cmdr=cmdr, hash=self.sha1sum, ext=ext)

    # utility fields
    sha1sum = models.CharField(unique=True, max_length=40, blank=True, editable=False)

    # filesystem
    image = ImageField(upload_to=waypoint_folder, height_field='img_height', width_field='img_width')

    orig_filename = models.CharField('original filename', max_length=768)
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True)

    # image meta
    img_height = models.IntegerField('image height')
    img_width = models.IntegerField('image width')

    # expedition meta
    desc = models.CharField('description', max_length=768, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    waypoint = models.ForeignKey(Waypoint, on_delete=models.SET_NULL, null=True, blank=True)

    # user
    owner = models.ForeignKey(Commander, on_delete=models.SET_NULL, null=True)

    # image uses
    public = models.BooleanField('display publicly', default=False)
    edited = models.BooleanField('edited', default=False)

    # imgur
    imgur_url = models.CharField('link to imgur upload', max_length=512, null=True, blank=True)
    del_hash = models.CharField('imgur deletion hash', max_length=512, null=True, blank=True)

    # todo: when creating LocationForm, auto-populate from parsed image filename
    # todo: add "validated" field and create script to manually approve and then upload to imgur

    def save(self, *args, **kwargs):

        # if file is new, store sha1sum and then watermark
        if not self.pk:
            sha1 = hashlib.sha1()
            for chunk in self.image.chunks():
                sha1.update(chunk)
            self.sha1sum = sha1.hexdigest()

            # open image in pillow for editing
            orig_path = self.image.path
            img = PImage.open(self.image.file)

            # resize if greater than 4k
            basewidth = 3840
            resize_factor = basewidth / float(img.width)
            if img.width > 3840:
                img = img.resize((basewidth, round(img.height * resize_factor)))

            # watermark
            # open watermark file
            wmk = PImage.open(str(SITE_ROOT/'static/watermark_margin.png'))

            # calculate watermark width relative to 4k image width
            wmk_ratio = wmk.width / basewidth
            new_wmk_width = wmk_ratio * img.width
            wmk_resize_factor = new_wmk_width / float(wmk.width)
            new_wmk_height = wmk_resize_factor * wmk.height
            wmk = wmk.resize((round(new_wmk_width), round(new_wmk_height)))

            # calculate position and watermark original image
            pos = [img.size[i] - wmk.size[i] for i in [0, 1]]
            img.paste(wmk, box=pos, mask=wmk)

            # open output stream and save image
            stream = io.BytesIO()
            img.save(stream, format='jpeg', dpi=(72, 72), quality=95)

            # create new django file wrapper for image
            self.image = InMemoryUploadedFile(file=stream, field_name='image',
                                              name=Path(orig_path).with_suffix('.jpg'),
                                              content_type='image/jpeg', size=stream.getbuffer().nbytes,
                                              content_type_extra=None, charset=None)

            # save changes to db
            super(Image, self).save(*args, **kwargs)


# delete the image file when the Image instance is deleted by the admin panel.
@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    try:
        delete(instance.image.file)   # delete thumbnail and source file
        # instance.image.delete(False)  # pass False to ensure that a save() isn't called.

    # if file is already gone, just ignore the error
    except FileNotFoundError:
        pass

