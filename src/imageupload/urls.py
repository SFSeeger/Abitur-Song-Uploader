from django.urls import include, path

from .views import (
    ProfileCreateView,
    ProfileDetailView,
    ProfileUpdateView,
    UserImageCreateView,
    UserImageUpdateView,
)

urlpatterns = [
    path(
        "image/<int:image_type>/",
        UserImageCreateView.as_view(),
        name="create-user-image",
    ),
    path(
        "image/update/<int:pk>/",
        UserImageUpdateView.as_view(),
        name="update-user-image",
    ),
    path("create/", ProfileCreateView.as_view(), name="create-profile"),
    path("update/<int:pk>/", ProfileUpdateView.as_view(), name="update-profile"),
    path("view/<int:pk>/", ProfileDetailView.as_view(), name="detail-profile"),
]
