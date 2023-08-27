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
from wine_store.cart.api.permissions import IsCartOwner
from wine_store.cart.api.serializers import CartItemReadSerializer, CartItemSerializer, CartModelSerializer
from wine_store.cart.models import Cart, CartItem


class CartViewSet(GenericViewSet):
    """Cart view set."""

    serializer_class = CartModelSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]
    http_method_names = ["get", "post"]

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


class CartItemViewSet(ModelViewSet):
    """Cart item view set."""

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]

    def get_serializer_class(self):
        """Return serializer based on action."""
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

    def perform_update(self, serializer):
        cart = Cart.objects.filter(user=self.request.user).first()
        serializer.save(cart=cart)

    def perform_destroy(self, instance):
        cart = Cart.objects.filter(user=self.request.user).first()
        cart.total -= instance.product.price * instance.quantity
        cart.save()
        instance.delete()
