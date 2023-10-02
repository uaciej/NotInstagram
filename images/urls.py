from django.urls import path
from .views import ImageUploadView, UserImagesList, signed_image_view

urlpatterns = [
    path("images/", UserImagesList.as_view()),
    path("upload/", ImageUploadView.as_view(), name="image_upload"),
    path(
        "signed_image_view/<str:signed_value>/",
        signed_image_view,
        name="signed_image_view",
    ),
]
