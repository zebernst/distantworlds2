from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import *


# Create your views here.
class ImageUploadView(LoginRequiredMixin, generic.FormView):
    form_class = ImageForm
    template_name = 'images/upload_form.html'
    success_url = reverse_lazy('astrophotography:gallery')  # todo: success_url -> location form

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user.commander  # save user
            instance.save()

            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class UserImageGalleryView(generic.ListView):
    model = Image


class PublicImageGalleryView(generic.ListView):
    template_name = 'images/gallery.html'

    def get_queryset(self):
        return Image.objects.filter(public=True)
