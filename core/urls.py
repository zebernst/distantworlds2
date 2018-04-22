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
    path('expedition/distantworlds2/', DistantWorlds2View.as_view(), name='distantworlds2'),
    path('expedition/cg-proposal/', CGProposalView.as_view(), name='cg-proposal'),
    path('expedition/background/', BackgroundView.as_view(), name='background'),
    path('info/contact/', ContactView.as_view(), name='contact'),
    path('info/fleetcomm/', FleetcommView.as_view(), name='fleetcomm'),
    path('info/order/', OrderView.as_view(), name='order'),

    path('ajax/roster', RosterDataJSON, name='roster_ajax'),
    path('success/', Success.as_view(), name='success'),
]
