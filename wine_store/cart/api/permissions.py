"""
Permissions for cart app
"""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsCartOwner(BasePermission):
    """Allow access only to cart owners."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user is cart owner."""
        return request.user == obj.user


class IsCarItemOwner(BasePermission):
    """Allow access only to cart owners."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user is cart owner."""
        return request.user == obj.cart.user
