# Django Rest Framework
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from wine_store.products.api.pagination import ProductPagination

# Products
from wine_store.products.api.serializers import ProductReviewSerializer, ProductSerializer
from wine_store.products.models import Product, ProductReview

# Utils
from wine_store.utils.permissions import IsOwner


class ProductView(ListModelMixin, GenericViewSet, RetrieveModelMixin):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True).order_by("total_rating")
        return queryset


class ProductReviewView(ModelViewSet):
    serializer_class = ProductReviewSerializer

    def get_permissions(self):
        permissions = [IsAuthenticatedOrReadOnly]
        if self.action in ["list", "retrieve"]:
            permissions = [AllowAny]
        elif self.action in ["create"]:
            permissions = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            permissions = [IsAuthenticated, IsOwner]

        return [permission() for permission in permissions]

    def get_queryset(self):
        if self.action == "list":
            return ProductReview.objects.filter(product=self.kwargs["wine_pk"])
        elif self.action is ["update", "partial_update", "destroy", "retrieve"]:
            return ProductReview.objects.filter(product=self.kwargs["wine_pk"], user=self.request.user)

        return ProductReview.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs["wine_pk"])

    def perform_update(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs["wine_pk"])
