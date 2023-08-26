"""
User models for Wine Store.
- User: Default custom user model for Wine Store.
- UserAddress: User address model.
- UserPayment: User payment model.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Wine Store.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = models.CharField(_("First Name"), blank=True, max_length=255)
    last_name = models.CharField(_("Last Name"), blank=True, max_length=255)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class UserAddress(models.Model):
    """UserAddress model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    default = models.BooleanField(default=True)
    delivery_instructions = models.TextField(blank=True, null=True)

    class Meta:
        """Meta options."""

        verbose_name = _("User Address")
        verbose_name_plural = _("User Addresses")

    def __str__(self):
        """Return user address."""
        return f"User Address: {self.id}"


class UserPayment(models.Model):
    """UserPayment model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    default = models.BooleanField(default=True)

    class Meta:
        """Meta options."""

        verbose_name = _("User Payment")
        verbose_name_plural = _("User Payments")

    def __str__(self):
        """Return user payment."""
        return f"User Payment: {self.id}"
