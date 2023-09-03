"""
Cart Serializers
"""


# Django REST Framework
from rest_framework.serializers import ModelSerializer

# Models
from wine_store.cart.models import Cart, CartItem

# Product
from wine_store.products.api.serializers import ProductSerializer


class CartItemReadSerializer(ModelSerializer):
    """Cart item model serializer."""

    product = ProductSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = CartItem
        fields = "__all__"


class CartItemSerializer(ModelSerializer):
    """Cart item model serializer."""

    class Meta:
        """Meta class."""

        model = CartItem
        fields = "__all__"
        read_only_fields = ["cart"]


class CartModelSerializer(ModelSerializer):
    """Cart model serializer."""

    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Cart
        fields = "__all__"
