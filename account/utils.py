import json
import os

import requests
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import RefreshToken


def get_auth_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
