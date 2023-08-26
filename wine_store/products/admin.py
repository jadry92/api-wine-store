"""
Wine Products Admin
"""

# Django
from django.contrib import admin

# Models
from wine_store.products.models import Product, ProductDiscount, ProductInventory, ProductReview


@admin.register(Product, ProductInventory, ProductReview, ProductDiscount)
class ProductAdmin(admin.ModelAdmin):
    pass
