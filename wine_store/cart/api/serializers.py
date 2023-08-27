"""
Cart Serializers
"""

# Django
from django.db.models import F, Sum

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

    def create(self, validate_data):
        cart_item = CartItem.objects.create(**validate_data)
        cart = Cart.objects.filter(user=self.context["request"].user).first()
        cart.total += cart_item.product.price * cart_item.quantity
        cart.save()
        return cart_item

    def update(self, instance, validated_data):
        cart_item = super().update(instance, validated_data)
        cart = Cart.objects.filter(user=self.context["request"].user).first()
        all_items = (
            CartItem.objects.filter(cart=cart)
            .annotate(value=F("product__price") * F("quantity"))
            .aggregate(total=Sum("value"))
        )
        cart.total = all_items["total"]
        cart.save()
        return cart_item


class CartModelSerializer(ModelSerializer):
    """Cart model serializer."""

    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Cart
        fields = "__all__"
