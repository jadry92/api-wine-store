"""
Order models.
- Order
- OrderItem
- OrderPayment
"""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# User
from wine_store.users.models import User, UserAddress


class Order(models.Model):
    """Order model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, related_name="orders", null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options."""

        verbose_name = _("Order Detail")
        verbose_name_plural = _("Order Details")

    def __str__(self):
        """Return order detail."""
        return f"Order Detail: {self.id}"

    def calculate_total(self):
        """Calculate total."""
        total = 0
        for item in self.items.all():
            total += item.price * item.quantity
        return total


class OrderPayment(models.Model):
    """OrderPayment model."""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_provider = models.CharField(max_length=255)
    payment_register = models.CharField(max_length=255, unique=True, null=True)
    payment_status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options."""

        verbose_name = _("Order Payment")
        verbose_name_plural = _("Order Payments")

    def __str__(self):
        """Return order payment."""
        return f"Order Payment: {self.id}"


class OrderItem(models.Model):
    """OrderItem model."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    SKU = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        """Meta options."""

        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        """Return order item."""
        return f"Order Item: {self.id}"
