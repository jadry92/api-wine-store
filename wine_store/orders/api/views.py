"""
    Orders API Views
"""

# Logger
import logging

# Rest Framework
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

logger = logging.getLogger(__name__)


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
        if cart.items.count() == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order_detail = serializer.save(user=self.request.user, total=cart.total, order_status="processing")
        # Create order items
        cart_items = CartItem.objects.filter(cart=cart)
        total = 0.0
        for cart_item in cart_items:
            OrderItem.objects.create(
                order_detail=order_detail,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )
            total += +float(cart_item.product.price) * float(cart_item.quantity)

        if total != float(cart.total):
            logger.error("Total of order is not equal to total of cart")

        payment_method_id = self.request.data.get("payment_method_id")
        payment = UserPayment.objects.get(id=payment_method_id)

        # Create order payment
        OrderPayment.objects.create(
            order_detail=order_detail,
            payment_method=payment,
            total=total,
            payment_status="pending",
            payment_register=f"O-id-{order_detail.id}-{payment.provider}-{payment.payment_method}",
        )
        # Delete cart
        cart.delete()
        # create new cart
        Cart.objects.create(user=self.request.user)
