from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import AddProductSerializer, ProductSerializer


class ListProducts(APIView):

    def get(self, request):
        products = Product.objects.filter(is_published=True).order_by("?")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class AdminListProducts(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({"detail": "Product Added!"}, status.HTTP_201_CREATED)
        raise serializers.ValidationError(serializer.errors)


class UpdateProductView(APIView):
    def put(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Invalid product!"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AddProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Product updated successfully!"}, status=status.HTTP_200_OK
            )

        raise serializers.ValidationError(serializer.errors)
