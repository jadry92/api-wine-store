"""
    Orders API Views
"""

# Rest Framework
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

# Cart
from wine_store.cart.models import Cart, CartItem
from wine_store.orders.api.serializers import OrderSerializer

# Orders
from wine_store.orders.models import OrderDetail, OrderItem, OrderPayment

# Users
from wine_store.users.models import UserPayment

# Utils
from wine_store.utils.permissions import IsOwner


class OrderViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    """Order view set."""

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Return orders for current user."""
        orders = OrderDetail.objects.filter(user=self.request.user)
        return orders

    def perform_create(self, serializer):
        """Create a new order."""
        cart = Cart.objects.get(id=self.request.user.cart.id)
        order_detail = serializer.save(user=self.request.user, total=cart.total, order_status="processing")
        # Create order items
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order_detail=order_detail,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )

        payment_method_id = self.request.data.get("payment_method_id")
        payment = UserPayment.objects.get(id=payment_method_id)

        # Create order payment
        OrderPayment.objects.create(
            order_detail=order_detail,
            payment_method=payment,
            total=order_detail.total,
            payment_status="pending",
            payment_register=f"O-id-{order_detail.id}-{payment.provider}-{payment.payment_method}",
        )
        # Delete cart
        cart.delete()
        # create new cart
        Cart.objects.create(user=self.request.user)
