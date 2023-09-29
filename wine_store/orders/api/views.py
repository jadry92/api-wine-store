"""
    Orders API Views
"""

# Logger
import logging

# Rest Framework
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

# Cart
from wine_store.cart.models import Cart
from wine_store.orders.api.serializers import OrderReadModelSerializer, OrderSerializer

# Orders
from wine_store.orders.models import OrderDetail

# Utils
from wine_store.utils.permissions import IsOwner

# Users


logger = logging.getLogger(__name__)


class OrderViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    """Order view set."""

    permission_classes = [IsAuthenticated, IsOwner]

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == "retrieve" or self.action == "list":
            return OrderReadModelSerializer
        return OrderSerializer

    def get_queryset(self):
        """Return orders for current user."""
        orders = OrderDetail.objects.filter(user=self.request.user)
        return orders

    def perform_create(self, serializer):
        """Create order."""
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(user=self.request.user, cart=cart)
        cart.delete()
        Cart.objects.create(user=self.request.user)
