from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Category
from .serializers import ProductSerializer

class ListProducts(APIView):

    def get(self, request):
        products = Product.objects.filter(is_published=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
