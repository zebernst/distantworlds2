from django import forms
from django.core.exceptions import ValidationError

from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image", "public", "edited", "desc")  # "waypoint", "location")

    def clean(self):
        cleaned_data = super().clean()

        try:
            file = cleaned_data['image']

            # calculate sha1sum
            sha1 = hashlib.sha1()
            for chunk in file.chunks():
                sha1.update(chunk)
            sha1sum = sha1.hexdigest()

            # reject duplicate images
            if Image.objects.filter(sha1sum=sha1sum).exists():
                raise ValidationError('Duplicate image detected. Please contact an admin for more information.')

            # reject low-res images
            min_width = 1280  # px
            if file.image.width < min_width:
                raise ValidationError('Image is too small. Please submit '
                                      'images that are at least {}px across.'.format(min_width))

        # in case there isn't an image that was uploaded
        except KeyError:
            pass

# todo: create LocationForm and add it to the ImageForm view like i did with the RegistrationForm
