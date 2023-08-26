# django
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

# rest_framework
from rest_framework.viewsets import ModelViewSet

from wine_store.users.api.permissions import IsAddressOwner

# users
from wine_store.users.api.serializers import UserAddressSerializer
from wine_store.users.models import UserAddress

User = get_user_model()


class UserAddressViewSet(ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated, IsAddressOwner]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
