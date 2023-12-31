from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ImageSerializer, ImageUploadSerializer
from .models import Image
from not_instagram.settings import BASE_DIR
from PIL import Image as PILImage
from django.core import signing
from django.urls import reverse
from django.core.files.base import ContentFile
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
import os
from datetime import datetime, timedelta


class ImageUploadView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ImageUploadSerializer

    def post(self, request, format=None):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_ext = os.path.splitext(request.data["file"].name)[
                1
            ]  # Get the file extension
            if file_ext.lower() not in [".jpg", ".jpeg", ".png"]:
                return Response(
                    {
                        "detail": "Invalid file type. Only .jpg, .jpeg, and .png files are allowed."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            image = serializer.save(user=request.user)
            thumbnail_urls = self.create_thumbnails(image)
            response_data = serializer.data
            response_data.update(thumbnail_urls)
            # Generate expiring link if link is enabled
            if request.user.tier.expiring_link_enabled:
                expiration_time = int(request.data.get("expiration_time", 300))
                expiration_time = max(300, min(expiration_time, 30000))
                link = self.generate_expiring_link(image, expiration_time)
                response_data["expiration_link"] = link
            # Delete the original file if link not enabled
            if not request.user.tier.link_enabled:
                os.remove(image.file.path)
                image.delete()
                del response_data["file"]

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_thumbnails(self, image):
        user_tier = image.user.tier
        thumbnail_sizes = user_tier.thumbnail_sizes
        thumbnail_urls = {}
        if thumbnail_sizes:  # Check if thumbnail_sizes is not empty
            thumbnail_sizes = thumbnail_sizes.split(",")
            for size in thumbnail_sizes:
                url = self.create_thumbnail(image, int(size))
                thumbnail_urls[f"url_{size}"] = url
        return thumbnail_urls

    def create_thumbnail(self, image, size):
        img = PILImage.open(image.file.path)
        img.thumbnail((size, size))

        # Save the thumbnail to a new file
        thumbnail_io = BytesIO()
        img_format = (
            img.format
        )  # This will be 'JPEG' for .jpg files and 'PNG' for .png files
        img.save(thumbnail_io, format=img_format)

        # Create a new Image instance and save the file to it
        thumbnail = Image(user=image.user)
        filename_base, filename_ext = os.path.splitext(
            os.path.basename(image.file.name)
        )
        file_name = f"{filename_base}_thumbnail_{size}{filename_ext}"
        thumbnail.file.save(file_name, ContentFile(thumbnail_io.getvalue()), save=False)
        thumbnail.save()
        return thumbnail.file.url

    def generate_expiring_link(self, image, expiration_time):
        # Create a signer
        signer = signing.TimestampSigner()

        # Calculate the expiration timestamp
        expiration_timestamp = (
            datetime.now() + timedelta(seconds=expiration_time)
        ).timestamp()

        # Sign the image id along with the expiration timestamp
        value = f"{image.id}:{expiration_timestamp}"
        signed_value = signer.sign(value)

        # Generate the URL for the view that will handle the signed link
        link = reverse("signed_image_view", args=[signed_value])

        return link


class UserImagesList(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        return (
            Image.objects.filter(user=self.request.user)
            .exclude(file__isnull=True)
            .exclude(file="")
        )


def image_view(request, filename):
    print(filename)
    image = get_object_or_404(Image, file=f"image_files/{filename}")
    print(image)
    return FileResponse(open(os.path.join(BASE_DIR, image.file.path), "rb"))


def signed_image_view(request, signed_value):
    # Create a signer
    signer = signing.TimestampSigner()

    # Try to unsign the value
    try:
        value = signer.unsign(signed_value)
    except signing.BadSignature:
        raise Http404("Invalid link")

    # Split the value into the image id and the expiration time
    image_id, expiration_timestamp = value.split(":")

    # Check if the link has expired
    expiration_time = datetime.fromtimestamp(float(expiration_timestamp))
    if datetime.now() > expiration_time:
        raise Http404("Expired link")

    # Get the image
    image = get_object_or_404(Image, id=image_id)

    # Determine the content type based on the file extension
    file_ext = os.path.splitext(image.file.name)[1].lower()
    if file_ext in [".jpg", ".jpeg"]:
        content_type = "image/jpeg"
    elif file_ext == ".png":
        content_type = "image/png"

    # Open the image file and return it as a response
    with open(image.file.path, "rb") as img:
        return HttpResponse(img.read(), content_type=content_type)
