from django.urls import path, include

from .views import UserImageCreateView, UserImageUpdateView

urlpatterns = [
    path("<int:image_type>/", UserImageCreateView.as_view(), name="create-user-image"),
    path("update/<int:pk>/", UserImageUpdateView.as_view(), name="update-user-image"),
]
