import os

from dotenv import load_dotenv

from business.models import Category, FAQ

load_dotenv()


def get_contact_details(request):
    return {
        "PHONE_NUMBER": os.getenv("PHONE_NUMBER"),
        "WHATSAPP_LINK": os.getenv("WHATSAPP_LINK"),
        "SHOP_EMAIL": os.getenv("SHOP_EMAIL"),
        "SHOP_ADDRESS": os.getenv("SHOP_ADDRESS"),
        "STORE_NAME": os.getenv("STORE_NAME"),
        "STORE_LOGO": os.getenv("STORE_LOGO"),
        "CONTACT_US": os.getenv("CONTACT_US"),
    }


def get_categories(request):
    categories = Category.objects.all()
    return {"categories": categories}


def get_faqs(request):
    faqs = FAQ.objects.all()
    return {"faqs": faqs}
