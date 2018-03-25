from django import forms

from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image", "public", "edited", "desc")  # "waypoint", "location")

# todo: create LocationForm and add it to the ImageForm view like i did with the RegistrationForm
