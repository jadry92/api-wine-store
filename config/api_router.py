# Django
from django.conf import settings
from django.urls import include, path

# Django Rest Framework
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
    path("users/", include("wine_store.users.api.urls")),
    path("wines/", include("wine_store.products.api.urls")),
    path("cart/", include("wine_store.cart.api.urls")),
] + router.urls
