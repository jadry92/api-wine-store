# Django
from django.conf import settings

# Django Rest Framework
from rest_framework.routers import DefaultRouter, SimpleRouter

# Products
from wine_store.products.api.views import ProductViewSet

# Users
from wine_store.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("wines", ProductViewSet, basename="wines")

app_name = "api"
urlpatterns = router.urls
