from django.urls import path

from .views import *

app_name = 'astrophotography'
urlpatterns = [
    path('upload/', ImageUpload.as_view(), name='upload-image'),
    path('success/', Success.as_view(), name='success'),
    path('register/', SignUpView.as_view(), name='register'),
]