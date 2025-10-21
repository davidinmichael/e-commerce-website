from django.urls import path

from .views import ListProducts, AdminListProducts

urlpatterns = [
    path("products/", ListProducts.as_view()),
    path("admin-products/", AdminListProducts.as_view()),
]
