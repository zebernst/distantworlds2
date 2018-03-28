from django.urls import path

from .views import *

app_name = 'astrophotography'
urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='upload-image'),
    path('gallery/', PublicImageGalleryView.as_view(), name='gallery')
]