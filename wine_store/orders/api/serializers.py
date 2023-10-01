"""
    Order Serializers
"""

# Utils
import hashlib
from random import randint
from time import sleep

# Rest Framework
from rest_framework import serializers

# Cart
from wine_store.cart.api.serializers import CartModelSerializer
from wine_store.cart.models import CartItem

# Order
from wine_store.orders.models import Order, OrderItem, OrderPayment
from wine_store.users.api.serializers import UserAddressModelSerializer

# User
from wine_store.users.models import UserAddress, UserPayment


class OrderModelSerializer(serializers.ModelSerializer):
    """Order serializer."""

    class Meta:
        """Meta options."""

        model = Order
        fields = "__all__"
        read_only_fields = ["user", "total", "order_status", "created_at", "updated_at"]


class OrderItemModelSerializer(serializers.ModelSerializer):
    """Order item serializer."""

    class Meta:
        """Meta options."""

        model = OrderItem
        fields = "__all__"
        read_only_fields = ["order", "product", "quantity", "price"]


class OrderPaymentModelSerializer(serializers.ModelSerializer):
    """Order payment serializer."""

    class Meta:
        """Meta options."""

        model = OrderPayment
        fields = "__all__"
        read_only_fields = ["order", "total", "payment_method"]


class OrderReadModelSerializer(serializers.ModelSerializer):
    """Order Detail read serializer."""

    user = serializers.StringRelatedField()
    shipping_address = UserAddressModelSerializer(many=False, read_only=True)
    payment = OrderPaymentModelSerializer(many=False, read_only=True)
    items = OrderItemModelSerializer(many=True, read_only=True)

    class Meta:
        """Meta options."""

        model = Order
        fields = "__all__"
        read_only_fields = ["user", "total", "order_status", "created_at", "updated_at"]


class OrderSerializer(serializers.Serializer):
    """Order serializer."""

    shipping_address = serializers.IntegerField()
    payment_method = serializers.IntegerField()
    cart = CartModelSerializer(many=False, write_only=True)

    def validate_shipping_address(self, value):
        try:
            user_address = UserAddress.objects.get(id=value)
            return user_address
        except UserAddress.DoesNotExist:
            raise serializers.ValidationError("The user address does not exist")

    def validate_payment_method(self, value):
        try:
            user_payment = UserPayment.objects.get(id=value)
            return user_payment
        except UserPayment.DoesNotExist:
            raise serializers.ValidationError("The user payment does not exist")

    def validate(self, data):
        items = CartItem.objects.filter(cart=data["cart"])
        if len(items) == 0:
            raise serializers.ValidationError("The cart is empty")
        self.context["items"] = items
        data["total"] = 0
        data["order_status"] = "PENDING"
        return data

    def create(self, validated_data):
        """Create order."""
        user_payment = validated_data.pop("user_payment")
        # Create order detail
        order = Order.objects.create(**validated_data)
        # Create order items
        items = self.context["items"]
        for item in items:
            OrderItem.objects.create(
                order=order,
                name=item.product.name,
                SKU=item.product.SKU,
                quantity=item.quantity,
                price=item.price,
            )
        # making payment
        order.total = order.calculate_total()
        order.save()
        payment_status, payment_register = self.make_request_payment(user_payment, order.total)
        OrderPayment.objects.create(
            order=order,
            total=order.total,
            payment_provider=user_payment.payment_provider,
            payment_register=payment_register,
            payment_status=payment_status,
        )

        return order

    def update(self, instance, validated_data):
        """Update order."""
        # update order address
        instance.shipping_address = validated_data.get("shipping_address", instance.shipping_address)
        instance.save()
        # try payment again
        if instance.payment.payment_status == "FAILED":
            user_payment = validated_data.pop("user_payment")
            payment_status, payment_register = self.make_request_payment(user_payment, instance.total)
            instance.payment.payment_register = payment_register
            instance.payment.payment_status = payment_status
            instance.payment.save()

        return instance

    def make_request_payment(self, user_payment, total):
        """Make request payment.
        This is a function simulate the interaction with a payment gateway.
        """
        sleep(5)
        success_flag = True if randint(0, 10) < 8 else False
        if success_flag:
            sha_payment = hashlib.sha256(
                f"{user_payment.id}+{user_payment.provider}+{user_payment.payment_method}+{total}".encode()
            )
            payment_register = sha_payment.hexdigest()
            return ("SUCCESS", payment_register)
        else:
            return ("FAILED", None)
