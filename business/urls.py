from django.urls import path

from .views import ListProducts, AdminListProducts, UpdateProductView

urlpatterns = [
    path("products/", ListProducts.as_view()),
    path("admin-products/", AdminListProducts.as_view()),
    path("admin-product/edit/<str:slug>/", UpdateProductView.as_view()),
]
