from django.urls import path
from .views import ImageUploadView, UserImagesList, image_view, signed_image_view

urlpatterns = [
    path("images/", UserImagesList.as_view(), name="user_images_list"),
    path("upload/", ImageUploadView.as_view(), name="image_upload"),
    path("media/image_files/<str:filename>/", image_view, name="image_view"),
    path(
        "signed_image_view/<str:signed_value>/",
        signed_image_view,
        name="signed_image_view",
    ),
]
