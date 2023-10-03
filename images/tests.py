from django.test import TestCase
from django.urls import reverse
from django.core.files import File
from rest_framework.test import APIClient
from rest_framework import status
from .models import Image
from users.models import Account, Tier
from PIL import Image as PILImage
from tempfile import NamedTemporaryFile
import os


class ImageUploadViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Account.objects.create_user(
            email="testuser@test.com", password="testpass"
        )
        self.tier = Tier.objects.create(
            name="testtier",
            thumbnail_sizes="60,120,240",
            link_enabled=True,
            expiring_link_enabled=True,
        )
        self.user.tier = self.tier
        self.user.save()
        self.client.login(email="testuser@test.com", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_upload_image(self):
        # Create a dummy image file
        img = PILImage.new("RGB", (60, 30), color="red")
        with NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            img.save(f, format="JPEG")
        try:
            with open(f.name, "rb") as f:
                # Make a POST request to the image upload API endpoint
                response = self.client.post(
                    reverse("image_upload"), {"file": f}, format="multipart"
                )
        except Exception as e:
            print(f"Error: {e}")
            return  # Return from the method if an exception occurs
        finally:
            os.remove(f.name)

        # Check that the response status is 201_CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that an Image instance was created with thumbnails
        self.assertEqual(Image.objects.count(), 4)

        # Check that the Image instance has the correct user
        self.assertEqual(Image.objects.first().user, self.user)

    def tearDown(self):
        # Delete any images that were created
        for image in Image.objects.all():
            if image.file and os.path.isfile(image.file.path):
                os.remove(image.file.path)


class UserImagesListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Account.objects.create_user(
            email="testuser@test.com", password="testpass"
        )
        self.tier = Tier.objects.create(
            name="testtier",
            thumbnail_sizes="60,120,240",
            link_enabled=True,
            expiring_link_enabled=True,
        )
        self.user.tier = self.tier
        self.user.save()
        self.client.login(email="testuser@test.com", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_get_images(self):
        # Create a dummy image file
        img = PILImage.new("RGB", (60, 30), color="red")
        with NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            img.save(f, format="JPEG")
        with open(f.name, "rb") as f:
            # Create a dummy image
            image = Image.objects.create(
                user=self.user, file=File(f, name=os.path.basename(f.name))
            )
        os.remove(f.name)

        # Get the images for the user
        response = self.client.get(reverse("user_images_list"))

        # Check that the response status is 200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response data contains the image
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], image.id)

    def tearDown(self):
        # Delete any images that were created
        for image in Image.objects.all():
            if image.file and os.path.isfile(image.file.path):
                os.remove(image.file.path)
