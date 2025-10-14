import os
from dotenv import load_dotenv




def get_whatsapp_link(request):
    return {"WHATSAPP_LINK": os.getenv("WHATSAPP_LINK")}

def get_booking_link(request):
    return {"BOOKING_LINK": os.getenv("BOOKING_LINK")}
