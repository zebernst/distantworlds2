from django.urls import path

from .views import *

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('join/', FleetRegistrationView.as_view(), name='join'),
    path('news/', NewsView.as_view(), name='news'),
    path('fleet/roster/', RosterView.as_view(), name='roster'),
    path('fleet/stats/', FleetStatsView.as_view(), name='stats'),
    path('fleet/showcase/', FleetShowcaseView.as_view(), name='showcase'),
    path('theexpedition/distantworlds2/', DistantWorlds2View.as_view(), name='distantworlds2'),

    path('ajax/roster', RosterDataJSON, name='roster_ajax'),
    path('success/', Success.as_view(), name='success'),
]
