"""
Product serializers
- ProductSerializer
"""

# Django Rest Framework
from rest_framework import serializers

# Models
from wine_store.products.models import Product


class ProductSerializer(serializers.ListSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock", "image")
