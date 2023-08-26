"""
Product serializers
- ProductSerializer
"""

# Django Rest Framework
from rest_framework import serializers

# Models
from wine_store.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
