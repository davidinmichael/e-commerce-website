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
        context = {
            "product": product,
        }
        return render(request, "frontend/product_detail.html", context)
