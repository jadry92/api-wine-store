"""
Cart Models Module:
 - Cart
 - CartItem
"""

# Django
from django.db import models

# Product Model
from wine_store.products.models import Product

# User Model
from wine_store.users.models import User


class Cart(models.Model):
    """Cart Model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    """CartItem Model."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
