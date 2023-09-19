"""
Cart Serializers
"""


# Django REST Framework
from rest_framework.exceptions import ValidationError
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

    def validate_quantity(self, value):
        """Validate quantity."""
        if value <= 0:
            raise ValidationError("Quantity must be greater than zero")
        return value

    def create(self, validated_data):
        """Create cart item."""
        print(validated_data)
        cart = validated_data["cart"]
        product = validated_data["product"]
        quantity = validated_data["quantity"]
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item is not None:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        cart.calculate_total()
        return cart_item

    def update(self, instance, validated_data):
        """Update cart item."""
        if not validated_data.get("quantity"):
            raise ValidationError({"quantity": "This field is required"})
        instance.quantity = validated_data["quantity"]
        instance.save()
        instance.cart.calculate_total()
        return instance


class CartModelSerializer(ModelSerializer):
    """Cart model serializer."""

    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        """Meta class."""

        model = Cart
        fields = "__all__"
