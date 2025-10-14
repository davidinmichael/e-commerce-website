import os
from dotenv import load_dotenv
from business.models import Category


def get_whatsapp_link(request):
    return {"WHATSAPP_LINK": os.getenv("WHATSAPP_LINK")}

def get_booking_link(request):
    return {"BOOKING_LINK": os.getenv("BOOKING_LINK")}


def get_categories(request):
    categories = Category.objects.all()
    return {"categories": categories}
