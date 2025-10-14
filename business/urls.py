from django.urls import path

from .views import ListProducts

urlpatterns = [
    path("products/", ListProducts.as_view()),
]
