# django
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

# rest_framework
from rest_framework.viewsets import GenericViewSet, ModelViewSet

# users
from wine_store.users.api.serializers import UserAddressSerializer, UserPaymentSerializer
from wine_store.users.models import UserAddress

# utils
from wine_store.utils.permissions import IsOwner

User = get_user_model()


class UserAddressViewSet(ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPaymentViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    serializer_class = UserPaymentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
