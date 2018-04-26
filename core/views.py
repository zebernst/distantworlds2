from django.contrib.auth import login, authenticate
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import generic

from core.forms import *


class HomeView(generic.TemplateView):
    template_name = 'core/home.html'


class DistantWorlds2View(generic.TemplateView):
    template_name = 'core/distant-worlds-2.html'


class CGProposalView(generic.TemplateView):
    template_name = 'core/cg_proposal.html'


class FleetRegistrationView(generic.TemplateView):
    template_name = 'core/fleet_registration.html'


class BackgroundView(generic.TemplateView):
    template_name = 'core/background.html'


class FleetcommView(generic.TemplateView):
    template_name = 'core/fleetcomm.html'


class OrderView(generic.TemplateView):
    template_name = 'core/order.html'


class RosterView(generic.TemplateView):
    template_name = 'core/roster.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['timestamp'] = Commander.objects.latest('modified').modified
        context['commanders'] = Commander.objects.all()
        return context


class FAQView(generic.TemplateView):
    template_name = 'core/faq.html'


class AssetsView(generic.TemplateView):
    template_name = 'core/assets.html'


class ScoutingView(generic.TemplateView):
    template_name = 'core/scouting.html'


class LogisticsView(generic.TemplateView):
    template_name = 'core/logistics.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['timestamp'] = Commander.objects.latest('modified').modified
        context['commanders'] = Commander.objects.all()
        return context


class FleetStatsView(generic.TemplateView):
    template_name = 'core/fleet_stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ship_qset = Commander.objects\
            .exclude(ship_model='INVALID SHIP')\
            .values('ship_model')\
            .order_by('ship_model')\
            .annotate(n=Count('ship_model'))
        total_cmdrs = Commander.objects.exclude(ship_model='INVALID SHIP').count()

        # format ship type stats into javascript array (use |safe filter in template)
        context['ship_types'] = [{'ship': Commander.Ship.values.get(s['ship_model']),
                                  'num': s['n'],
                                  'percent': (s['n']/total_cmdrs)} for s in ship_qset]

        return context


class FleetShowcaseView(generic.TemplateView):
    template_name = 'core/showcase.html'


class ContactView(generic.TemplateView):
    template_name = 'core/contact.html'


class SignUpView(generic.FormView):
    # todo: https://simpleisbetterthancomplex.com/article/2017/08/19/how-to-render-django-form-manually.html#rendering-bootstrap-4-forms
    template_name = 'registration/register_form.html'
    success_url = '/success/'

    # return empty form
    def get(self, request, *args, **kwargs):
        user_form = UserForm(prefix='user')
        cmdr_form = CommanderForm(prefix='cmdr')
        return render(request, self.template_name, {'user_form': user_form, 'cmdr_form': cmdr_form})

    # process submitted form
    def post(self, request, *args, **kwargs):
        # process user portion of form
        user_form = UserForm(request.POST, prefix='user')
        cmdr_form = CommanderForm(request.POST, prefix='cmdr')  # created here in case user_form fails validation
        if user_form.is_valid() and cmdr_form.is_valid():  # validate
            # signal receiver creates and links a new Commander object on user_form.save(). The cmdr_form is
            # re-initialized with an instance of user.commander and its data is saved to that object.
            user = user_form.save()
            user.save()

            try:
                cmdr = Commander.objects.get(roster_num=cmdr_form.cleaned_data['roster_num'])
            except Commander.DoesNotExist:
                # todo: redirect to Register Commander form (need to create)
                cmdr = CommanderForm(request.POST, prefix='cmdr').save()  # , instance=user.commander)

            cmdr.user = user
            cmdr.save()

            # authenticate
            raw_pw = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_pw)
            login(request, user)
            return redirect(self.success_url)

        # if both forms are not valid, drop out of if clause and re-render form with errors
        return render(request, self.template_name, {'user_form': user_form, 'cmdr_form': cmdr_form})


# todo: make this better and parse the data and figure out the enums!!!!!!!!!
def RosterDataJSON(request):
    objects = Commander.objects.all().values()
    return JsonResponse({'data': list(objects)})


class Success(generic.TemplateView):
    template_name = 'success.html'
