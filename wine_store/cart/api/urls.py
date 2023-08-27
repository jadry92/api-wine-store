"""
URLs cart
"""

# Django
from django.urls import path

# Django REST Framework
from rest_framework.routers import SimpleRouter

# Views
from wine_store.cart.api.views import CartItemViewSet, CartViewSet

router = SimpleRouter()
router.register(r"items", CartItemViewSet, basename="cart_items")

urlpatterns = [path("", CartViewSet.as_view({"get": "get"}))] + router.urls
