"""
    Pagination for products
"""

# Django Rest Framework
from rest_framework.pagination import PageNumberPagination


class ProductPagination(PageNumberPagination):
    """Product pagination class."""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
    last_page_strings = ("last",)
