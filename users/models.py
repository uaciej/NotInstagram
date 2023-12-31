from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from rest_framework.authtoken.models import Token
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class AccountManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class Tier(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    thumbnail_sizes = models.CharField(
        _("Thumbnail Sizes"),
        max_length=100,
        blank=True,
    )
    link_enabled = models.BooleanField(_("Link Enabled"), default=False)
    expiring_link_enabled = models.BooleanField(
        _("Expiring Link Enabled"), default=False
    )

    def clean(self):
        super().clean()
        sizes = self.thumbnail_sizes.split(",")
        cleaned_sizes = []
        for size in sizes:
            if size:
                # Remove spaces
                size = size.replace(" ", "")
                # Check that size is an integer
                if not size.isdigit():
                    raise ValidationError(
                        {"thumbnail_sizes": _("All sizes must be integers.")}
                    )
                # Check that size is not greater than the maximum value
                if int(size) > 1920:
                    raise ValidationError(
                        {
                            "thumbnail_sizes": _(
                                "Thumbnail size must not exceed 1920 pixels."
                            )
                        }
                    )
            cleaned_sizes.append(size)
        # Assign the cleaned sizes back to thumbnail_sizes
        self.thumbnail_sizes = ",".join(cleaned_sizes)

    def __str__(self):
        return self.name


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    tier = models.ForeignKey(Tier, on_delete=models.SET(1), default=1)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email
