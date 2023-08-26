"""
URLs cart
"""

# Django

# Django REST Framework
from rest_framework.routers import SimpleRouter

# Views
from wine_store.cart.api.views import CartViewSet

router = SimpleRouter()
router.register("", CartViewSet)

urlpatterns = router.urls
