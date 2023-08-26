"""
Product models:
- Product
- ProductInventory
- ProductReview
- ProductDiscount
"""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# User
from wine_store.users.models import User


class ProductInventory(models.Model):
    """ProductInventory model."""

    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options."""

        verbose_name = _("Product Inventory")
        verbose_name_plural = _("Product Inventories")


class ProductDiscount(models.Model):
    """ProductDiscount model."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options."""

        verbose_name = _("Product Discount")
        verbose_name_plural = _("Product Discounts")

    def __str__(self):
        """Return product name."""
        return self.name


class Product(models.Model):
    """Product model."""

    name = models.CharField(max_length=255)
    description = models.TextField()
    SKU = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    discount = models.ForeignKey(ProductDiscount, on_delete=models.SET_NULL, null=True, blank=True)
    inventory = models.OneToOneField(ProductInventory, on_delete=models.CASCADE)
    total_rating = models.FloatField(default=0, null=True, blank=True)

    class Meta:
        """Meta options."""

        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        """Return product name."""
        return self.name


class ProductReview(models.Model):
    """ProductReview model."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta options."""

        verbose_name = _("Product Review")
        verbose_name_plural = _("Product Reviews")

    def __str__(self):
        """Return product name."""
        return self.product.name
