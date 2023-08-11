# Django Rest Framework
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from wine_store.products.api.serializers import ProductSerializer

# Products
from wine_store.products.models import Product


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
