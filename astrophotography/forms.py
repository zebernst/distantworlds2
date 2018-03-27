from django import forms
from django.core.exceptions import ValidationError

from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image", "public", "edited", "desc")  # "waypoint", "location")

    def clean(self):
        cleaned_data = super().clean()

        sha1 = hashlib.sha1()
        for chunk in cleaned_data['image'].chunks():
            sha1.update(chunk)
        sha1sum = sha1.hexdigest()

        if Image.objects.filter(sha1sum=sha1sum).exists():
            raise ValidationError('Duplicate image detected. Please contact an admin for more information.')

# todo: create LocationForm and add it to the ImageForm view like i did with the RegistrationForm
