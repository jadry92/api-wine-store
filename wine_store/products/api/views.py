# Django Rest Framework
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from wine_store.products.api.serializers import ProductSerializer

# Products
from wine_store.products.models import Product


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
