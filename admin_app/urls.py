from django.urls import path

from .views import (
    RegisterAdminView,
    LoginAdminView,
    DashboardView,
    AddProductView,
    EditProductView,
    DeleteProduct,
    CategoriesView,
    DeleteCategory,
)
from . import views
urlpatterns = [
    path("register/", RegisterAdminView.as_view(), name="register_admin"),
    path("login/", LoginAdminView.as_view(), name="login_admin"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("delete-category/<int:pk>/", DeleteCategory.as_view(), name="delete_category"),
    # path("add-category/", views.add_category_page, name="add_category"),
    path("products/", views.list_products, name="admin_products"),
    path("add-product/", AddProductView.as_view(), name="add_product"),
    path("edit-product/<str:slug>/", EditProductView.as_view(), name="edit_product"),
    path("delete-product/<str:slug>/", DeleteProduct.as_view(), name="delete_product"),
]
