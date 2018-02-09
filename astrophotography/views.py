from django.shortcuts import render, redirect
from django.views import generic

from .forms import *


# Create your views here.
class ImageUpload(generic.FormView):
    form_class = ImageForm
    template_name = 'images/upload_form.html'
    success_url = '/success/'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user.commander
            instance.save()

            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})
