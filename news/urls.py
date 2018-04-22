from django.urls import path

from news.views import *

app_name = 'news'
urlpatterns = [
    path('news/', NewsView.as_view(), name='news'),
]
