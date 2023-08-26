# rest_framework
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Return True if permission is granted to the user, False otherwise.
        """
        return obj.user == request.user
