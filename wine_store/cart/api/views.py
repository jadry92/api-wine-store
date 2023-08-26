"""
Cart Views
 - CartViewSet
    This view set allows create, delete, update and retrieve cart objects of the current user.
"""

# Django REST Framework
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

# Permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from wine_store.cart.api.permissions import IsCartOwner

# Serializers
from wine_store.cart.api.serializers import CartModelSerializer

# Models
from wine_store.cart.models import Cart


class CartViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin):
    """Cart view set."""

    serializer_class = CartModelSerializer
    lookup_field = "user__username"
    permission_classes = [IsAuthenticated, IsCartOwner]
    queryset = Cart.objects.all()

    def get_queryset(self):
        """Restrict list to only current user."""
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset
