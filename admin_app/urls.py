from django.urls import path

from .views import (
    RegisterAdminView,
    LoginAdminView,
    DashboardView,
    AddProductView,
    EditProductView,
    DeleteProduct,
)
from . import views
urlpatterns = [
    path("register/", RegisterAdminView.as_view(), name="register_admin"),
    path("login/", LoginAdminView.as_view(), name="login_admin"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("products/", views.list_products, name="admin_products"),
    path("add-product/", AddProductView.as_view(), name="add_product"),
    path("edit-product/<str:slug>/", EditProductView.as_view(), name="edit_product"),
    path("delete-product/<str:slug>/", DeleteProduct.as_view(), name="delete_product"),
]
