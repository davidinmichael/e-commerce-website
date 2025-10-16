from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from business.models import Product


def home_view(request):
    return render(request, "frontend/index.html")


class ProductDetail(View):

    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            messages.error(request, "Invalid product!")
            return redirect("home")
        category = product.category
        related_products = (
            Product.objects.filter(category=category).order_by("?")[:9]
            if category
            else []
        )
        print(f"Products: {related_products}")
        context = {
            "product": product,
            "related_products": related_products,
        }
        return render(request, "frontend/product_detail.html", context)
