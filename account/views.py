import os

from django.conf import settings
from django.template.loader import render_to_string
from dotenv import load_dotenv
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.choices import AccountStatus
from core.utils import generate_random_code, send_email

from .models import Account, AccountDeleteRequest
from .serializers import (
    ChangePasswordSerializer,
    CreateAccountSerializer,
    DeleteAccountSerializer,
    LoginSerializer,
    ReadAccountSerializer,
    SetasswordSerializer,
    VerifyAccountSetPasswordSerializer,
)
from .utils import get_auth_token

load_dotenv()
ALLOWED_ACCOUNT_STATUS = [AccountStatus.VERIFIED, AccountStatus.UNVERIFIED]
BASE_URL = settings.BASE_URL


class CreateAccountView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            context = {
                "name": user.first_name,
                "url": f"{BASE_URL}/?token={user.otp_token}",
            }
            template = render_to_string("account/otp_welcome_email.html", context)
            send_email(user.email, "RestInn: Confirm Account", template)
            print(f"OTP: {user.otp_token}")
            return Response(
                {"detail": "Account created! Email sent to your inbox."},
                status.HTTP_201_CREATED,
            )
        raise serializers.ValidationError(serializer.errors)


class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = Account.objects.get(email=email, is_deleted=False)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Invalid user account! Create an account to continue."},
                status.HTTP_404_NOT_FOUND,
            )
        if user.account_status not in ALLOWED_ACCOUNT_STATUS:
            return Response(
                {"detail": "Suspended or deleted account. Contact support for help!"},
                status.HTTP_404_NOT_FOUND,
            )
        user.otp_token = generate_random_code()
        user.save()
        context = {
            "name": user.first_name,
            "otp": user.otp_token,
        }
        template = render_to_string("account/otp.html", context)
        send_email(user.email, "dBookDraft: OTP", template)
        print(f"OTP: {user.otp_token}")
        return Response({"detail": "Email sent successfully!"}, status.HTTP_200_OK)


class VerifyAccountEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyAccountSetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)

        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        try:
            user = Account.objects.get(otp_token=token, is_deleted=False)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Invalid user account! Create an account to continue."},
                status.HTTP_404_NOT_FOUND,
            )
        if user.account_status not in ALLOWED_ACCOUNT_STATUS:
            return Response(
                {"detail": "Suspended or deleted account. Contact support for help!"},
                status.HTTP_404_NOT_FOUND,
            )
        user.is_email_verified = True
        user.account_status = AccountStatus.VERIFIED
        user.otp_token = ""
        user.set_password(password)
        user.save()
        context = {"name": user.first_name, "url": f"{BASE_URL}/login"}
        template = render_to_string("account/successful_welcome_email.html", context)
        send_email(user.email, f"RestInn: Welcome {user.first_name}!", template)
        data = {
            "detail": "Login successful!",
            "auth_token": get_auth_token(user),
        }
        return Response(data, status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")

            try:
                user = Account.objects.get(email=email, is_deleted=False)
            except Account.DoesNotExist:
                return Response(
                    {"detail": "Invalid user account!"},
                    status.HTTP_404_NOT_FOUND,
                )
            if user.is_deleted:
                return Response(
                    {
                        "detail": "Suspended or deleted account, contact support for further assistance!"
                    },
                    status.HTTP_400_BAD_REQUEST,
                )

            if user.account_status not in ALLOWED_ACCOUNT_STATUS:
                return Response(
                    {
                        "detail": "Suspended or deleted account. Contact support for help!"
                    },
                    status.HTTP_404_NOT_FOUND,
                )

            if user.check_password(password):
                if user.is_2fa_enabled:
                    user.otp_token = generate_random_code()
                    user.save()
                    context = {
                        "name": user.first_name,
                        "otp": user.otp_token,
                    }
                    template = render_to_string("account/otp_login.html", context)
                    send_email(user.email, "RestInn: Login OTP", template)
                    data = {
                        "detail": "OTP sent to your email!",
                        "is_2fa_enabled": user.is_2fa_enabled,
                    }
                    return Response(data, status.HTTP_200_OK)
                data = {
                    "detail": "Login successful!",
                    "is_2fa_enabled": user.is_2fa_enabled,
                    "auth_token": get_auth_token(user),
                }
                return Response(data, status.HTTP_200_OK)
            return Response(
                {"detail": "invalid email or password!"}, status.HTTP_400_BAD_REQUEST
            )
        raise serializers.ValidationError(serializer.errors)


class VerifyLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = str(request.data.get("token", "")).upper()
        try:
            user = Account.objects.get(otp_token=token, is_deleted=False)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Invalid user account! Create an account to continue."},
                status.HTTP_404_NOT_FOUND,
            )
        if user.account_status not in ALLOWED_ACCOUNT_STATUS:
            return Response(
                {"detail": "Suspended or deleted account. Contact support for help!"},
                status.HTTP_404_NOT_FOUND,
            )

        user.otp_token = ""
        user.save()

        data = {
            "detail": "Login successful!",
            "auth_token": get_auth_token(user),
        }
        return Response(data, status.HTTP_200_OK)


class UserDetailsView(APIView):

    def get(self, request):
        user = request.user
        serializer = ReadAccountSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data["password"]
            old_password = serializer.validated_data["old_password"]
            if user.check_password(old_password):
                user.set_password(password)
                user.save()
                return Response(
                    {"detail": "User password updated successfully!"},
                    status.HTTP_200_OK,
                )
            return Response(
                {"detail": "Old password not correct!"}, status.HTTP_400_BAD_REQUEST
            )

        raise serializers.ValidationError(serializer.errors)

    def put(self, request):
        print("Update user")
        instance = request.user
        serializer = CreateAccountSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "User details updated successfully!"}, status.HTTP_200_OK
            )
        raise serializers.ValidationError(serializer.errors)


class SetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SetasswordSerializer(data=request.data)
        if serializer.is_valid():
            token = str(serializer.validated_data.get("token")).upper()
            password = serializer.validated_data.get("password")
            try:
                user = Account.objects.get(otp_token=token, is_deleted=False)
            except Account.DoesNotExist:
                return Response(
                    {"detail": "Invalid user account! Create an account to continue."},
                    status.HTTP_404_NOT_FOUND,
                )

            if user.account_status not in ALLOWED_ACCOUNT_STATUS:
                return Response(
                    {
                        "detail": "Suspended or deleted account. Contact support for help!"
                    },
                    status.HTTP_404_NOT_FOUND,
                )

            user.otp_token = ""
            user.set_password(password)
            user.save()
            return Response(
                {"detail": "Password set successfully! Continue to login"},
                status.HTTP_200_OK,
            )
        raise serializers.ValidationError(serializer.errors)


class DeleteAccountView(APIView):

    def post(self, request):
        user = request.user
        serializer = DeleteAccountSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get("password", "")
            type_delete = serializer.validated_data.get("type_delete")
            reason = serializer.validated_data.get("reason", "")

            if user.check_password(password):
                AccountDeleteRequest.objects.create(user=user, reason=reason)
                user.is_deleted = True
                user.save()
                return Response(
                    {"detail": "Account deleted successfully!"}, status.HTTP_200_OK
                )
            return Response(
                {"detail": "Incorrect password!"}, status.HTTP_400_BAD_REQUEST
            )
        raise serializers.ValidationError(serializer.errors)
