"""
    Orders API URL Configuration
"""

from rest_framework.routers import SimpleRouter

from wine_store.orders.api.views import OrderViewSet

router = SimpleRouter()
router.register(r"", OrderViewSet, basename="orders")

urlpatterns = router.urls
