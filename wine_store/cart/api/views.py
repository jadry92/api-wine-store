"""
Cart Views
 - CartViewSet
    This view set allows create, delete, update and retrieve cart objects of the current user.
"""

# Django REST Framework
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

# Cart
from wine_store.cart.api.permissions import IsCarItemOwner, IsCartOwner
from wine_store.cart.api.serializers import CartItemReadSerializer, CartItemSerializer, CartModelSerializer
from wine_store.cart.models import Cart, CartItem


class CartViewSet(GenericViewSet):
    """Cart view set."""

    serializer_class = CartModelSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]

    def get_queryset(self):
        """Restrict list to only current user."""
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset

    def get_object(self):
        """Return cart of current user."""
        return self.get_queryset().first()

    def get(self, request, *args, **kwargs):
        """Return cart of current user."""
        cart = self.get_object()
        if cart is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CartModelSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """Delete cart of current user."""
        cart = self.get_object()
        if cart is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart.delete()
        cart = Cart.objects.create(user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(ModelViewSet):
    """Cart item view set."""

    permission_classes = [IsAuthenticated, IsCarItemOwner]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return CartItemReadSerializer
        return CartItemSerializer

    def get_queryset(self):
        """Restrict list to only current user."""
        queryset = CartItem.objects.filter(cart__user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Create cart item."""
        cart = Cart.objects.filter(user=self.request.user).first()
        serializer.save(cart=cart)

    def preform_update(self, serializer):
        """Update cart item."""
        cart = Cart.objects.filter(user=self.request.user).first()
        serializer.save(cart=cart)
