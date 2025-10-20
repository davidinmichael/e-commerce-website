from django.urls import path

from . import views
from .views import ProductDetail, CartPage

urlpatterns = [
    path("", views.home_view, name="home"),
    path("products/", views.products_page, name="products"),
    path("product/<str:slug>/", ProductDetail.as_view(), name="product_detail"),
    path("cart/", CartPage.as_view(), name="cart"),
]
