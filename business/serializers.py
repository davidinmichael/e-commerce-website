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


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "category",
            "description",
            "features",
            "price",
            "discount",
            "images",
            "featured_image",
            "inventory_count",
            "is_published",
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
