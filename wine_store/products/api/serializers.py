"""
Product serializers
- ProductSerializer
"""

# Django
from django.db.models import Avg

# Django Rest Framework
from rest_framework import serializers

# Models
from wine_store.products.models import Product, ProductDiscount, ProductInventory, ProductReview


class ProductDiscountSerializer(serializers.ModelSerializer):
    """ProductDiscount serializer."""

    class Meta:
        """Meta options."""

        model = ProductDiscount
        fields = "__all__"


class ProductInventorySerializer(serializers.ModelSerializer):
    """ProductInventory serializer."""

    class Meta:
        """Meta options."""

        model = ProductInventory
        fields = "__all__"


class ProductReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = ProductReview
        fields = "__all__"
        read_only_fields = ["user", "product"]

    def create(self, validated_data):
        product_review = ProductReview.objects.create(**validated_data)
        product_review.save()
        product = Product.objects.get(id=validated_data["product_id"])
        product.total_rating = product.reviews.aggregate(Avg("rating"))["rating__avg"]
        product.save()
        return product_review

    def update(self, instance, validated_data):
        product_review = super().update(instance, validated_data)
        product = Product.objects.get(id=validated_data["product_id"])
        product.total_rating = product.reviews.aggregate(Avg("rating"))["rating__avg"]
        product.save()
        return product_review


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer."""

    inventory = ProductInventorySerializer()
    discount = ProductDiscountSerializer()
    reviews = ProductReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
