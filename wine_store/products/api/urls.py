"""
URLs for the products app endpoint.
"""

# Django


# Rest Framework
from rest_framework.routers import SimpleRouter

# Views
from wine_store.products.api.views import ProductReviewView, ProductView

route = SimpleRouter()
route.register(r"", ProductView, basename="wines")
route.register(r"(?P<wine_pk>[^/.]+)/reviews", ProductReviewView, basename="wine-reviews")
app_name = "wines"

urlpatterns = route.urls
