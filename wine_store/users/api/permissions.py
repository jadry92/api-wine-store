"""
    User Custom Permissions
"""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAddressOwner(BasePermission):
    """Allow access only to address owners."""

    def has_object_permission(self, request, view, obj):
        """Check requesting user is address owner."""
        return request.user == obj.user
