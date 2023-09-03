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

# Products
from wine_store.products.models import Product


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


class CartItemViewSet(ModelViewSet):
    """Cart item view set."""

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsCarItemOwner]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return CartItemReadSerializer
        return CartItemSerializer

    def get_queryset(self):
        """Restrict list to only current user."""
        queryset = CartItem.objects.filter(cart__user=self.request.user)
        return queryset

    def get_object(self):
        """Return cart item of current user."""
        return self.get_queryset().first()

    def get_serializer_context(self):
        """Add cart to serializer context."""
        context = super().get_serializer_context()
        context["cart"] = Cart.objects.filter(user=self.request.user).first()
        return context

    def create(self, request, *args, **kwargs):
        """Create cart item."""
        context = self.get_serializer_context()
        cart = context["cart"]
        item = CartItem.objects.filter(cart=cart, product=request.data["product"]).first()
        if item is not None:
            item.quantity += int(request.data["quantity"])
            item.save()
            cart.total += item.product.price * int(request.data["quantity"])
            cart.save()
            serializer = self.get_serializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart=cart)
        product = Product.objects.get(id=serializer.data["product"])
        cart.total += product.price * serializer.data["quantity"]
        cart.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update cart item."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        cart = Cart.objects.filter(user=self.request.user).first()
        cart.total -= instance.product.price * instance.quantity
        cart.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        product = Product.objects.get(id=data["product"])
        cart.total += product.price * data["quantity"]
        cart.save()
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """Delete cart item."""
        instance = self.get_object()
        cart = Cart.objects.filter(user=self.request.user).first()
        cart.total -= instance.product.price * instance.quantity
        cart.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
