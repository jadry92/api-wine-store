"""
Cart Admin View
"""

# Django
from django.contrib import admin

# Cart
from wine_store.cart.models import Cart, CartItem


@admin.register(Cart, CartItem)
class CartAdmin(admin.ModelAdmin):
    """Cart Admin."""

    pass
