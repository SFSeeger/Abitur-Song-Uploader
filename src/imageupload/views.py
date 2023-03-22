from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from songuploader.utils import ConfiguredLoginViewMixin

from .forms import ProfileForm, UserImageForm
from .models import Profile, UserImage


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


class ProfileCreateView(ConfiguredLoginViewMixin, CreateView):
    model = Profile
    form_class = ProfileForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if profile := self.model.objects.filter(user=self.request.user).first():
            return redirect("detail-profile", pk=profile.pk)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: UserImageForm) -> HttpResponse:
        if profile := self.model.objects.filter(user=self.request.user).first():
            return redirect("detail-profile", pk=profile.pk)
        self.model.objects.create(
            **form.cleaned_data,
            user=self.request.user,
        )
        return redirect("detail-profile", pk=profile.id)


class ProfileUpdateView(ConfiguredLoginViewMixin, UpdateView):
    model = Profile
    form_class = ProfileForm

    def get_success_url(self) -> str:
        return reverse_lazy("detail-profile", pk=self.get_object().id)


class ProfileDetailView(DetailView):
    model = Profile
