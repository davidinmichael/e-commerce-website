from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category
from .serializers import ProductSerializer, AddProductSerializer
from rest_framework import serializers

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
