from django.urls import path

from . import views
from .views import ProductDetail

urlpatterns = [
    path("", views.home_view, name="home"),
    path("product/<str:slug>/", ProductDetail.as_view(), name="product_detail"),
]
