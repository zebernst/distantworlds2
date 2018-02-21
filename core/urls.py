from django.urls import path

from .views import *

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),

    path('success/', Success.as_view(), name='success'),


]
