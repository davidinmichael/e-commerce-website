from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from business.models import Product
from urllib.parse import quote
from dotenv import load_dotenv
import os
load_dotenv()


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
        message = f"Hello, I’m interested in this product:\n\n*{product.title}*\nPrice: ₦{product.price}"
        if product.discount > 0:
            message += f" ({product.discount}% OFF)"
        message += f"\n\nView it here: {request.build_absolute_uri()}"
        encoded_message = quote(message)
        whatsapp_number = os.getenv("WHATSAPP_NUMBER")

        context = {
            "product": product,
            "related_products": related_products,
            "whatsapp_link": f"https://wa.me/{whatsapp_number}?text={encoded_message}",
        }
        return render(request, "frontend/product_detail.html", context)
