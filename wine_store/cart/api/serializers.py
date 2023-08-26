"""
Cart Serializers
"""

# Django REST Framework
from rest_framework.serializers import ModelSerializer

# Models
from wine_store.cart.models import Cart


class CartModelSerializer(ModelSerializer):
    """Cart model serializer."""

    class Meta:
        """Meta class."""

        model = Cart
        fields = (
            "user",
            "total",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "user",
            "total",
            "created_at",
            "updated_at",
        )
