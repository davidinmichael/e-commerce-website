from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "category",
            "slug",
            "description",
            "features",
            "price",
            "discount",
            "images",
            "featured_image",
            "inventory_count",
            "is_published",
        ]
