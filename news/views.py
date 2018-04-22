# Create your views here.
from django.views import generic


class NewsView(generic.TemplateView):
    template_name = 'core/news.html'
