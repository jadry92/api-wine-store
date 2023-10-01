"""
    Orders API Views
"""

# Rest Framework
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

# Cart
from wine_store.cart.models import Cart
from wine_store.orders.api.serializers import OrderReadModelSerializer, OrderSerializer

# Orders
from wine_store.orders.models import Order

# Utils
from wine_store.utils.permissions import IsOwner


class OrderViewSet(ModelViewSet):
    """Order view set."""

    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "pk"

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == "retrieve" or self.action == "list":
            return OrderReadModelSerializer
        return OrderSerializer

    def get_queryset(self):
        """Return orders for current user."""
        orders = Order.objects.filter(user=self.request.user)
        return orders

    def perform_create(self, serializer):
        """Create order."""
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(user=self.request.user, cart=cart)
        cart.delete()
        Cart.objects.create(user=self.request.user)

    def perform_update(self, serializer):
        """Update order."""
        order = self.get_object()
        serializer.save(user=self.request.user, cart=order.cart)
