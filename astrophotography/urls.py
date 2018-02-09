from django.urls import path

from .views import *

app_name = 'astrophotography'
urlpatterns = [
    path('upload/', ImageUpload.as_view(), name='upload-image'),
]