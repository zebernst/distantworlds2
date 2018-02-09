from django.urls import path

from .views import *

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),

    # auth
    # path('login/', auth_views.login, name='login'),
    # path('logout/', auth_views.logout, name='logout'),
    path('register/', SignUpView.as_view(), name='register'),


    path('success/', Success.as_view(), name='success'),

]