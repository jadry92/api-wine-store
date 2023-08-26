"""
URLs for the products app endpoint.
"""

# Django
from django.urls import path

# Views
from wine_store.products.api.views import ProductListView

app_name = "products"

urlpatterns = [
    path("", view=ProductListView.as_view(), name="list"),
]
