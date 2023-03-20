from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from songuploader.utils import ConfiguredLoginViewMixin
from .forms import UserImageForm
from .models import UserImage

# Create your views here.
class UserImageCreateView(ConfiguredLoginViewMixin, CreateView):
    model = UserImage
    form_class = UserImageForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if image := self.model.objects.filter(user=self.request.user).first():
            return redirect("update-user-image", pk=image.pk)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: UserImageForm) -> HttpResponse:
        if image := self.model.objects.filter(user=self.request.user).first():
            return redirect("update-user-image", pk=image.pk)
        UserImage.objects.create(
            **form.cleaned_data,
            user=self.request.user,
            image_type=self.kwargs.get("image_type"),
        )
        return redirect("index")


class UserImageUpdateView(ConfiguredLoginViewMixin, UpdateView):
    model = UserImage
    form_class = UserImageForm
    success_url = reverse_lazy("index")
