"""
    Order Serializers
"""

# Rest Framework
from rest_framework.serializers import ModelSerializer

# Order
from wine_store.orders.models import OrderDetail


class OrderSerializer(ModelSerializer):
    """Order serializer."""

    class Meta:
        """Meta options."""

        model = OrderDetail
        fields = "__all__"
        read_only_fields = ["user", "total", "order_status", "created_at", "updated_at"]
