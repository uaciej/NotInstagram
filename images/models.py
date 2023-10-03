from django.db import models
from django.contrib.auth import get_user_model


class Image(models.Model):
    file = models.ImageField(upload_to="image_files/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), related_name="images", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Image {self.id} - User {self.user.email}"
