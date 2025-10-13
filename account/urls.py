from django.urls import path

from .views import (
    CreateAccountView,
    LoginView,
    UserDetailsView,
    DeleteAccountView,
    SendOTPView,
    VerifyAccountEmailView,
    VerifyLoginView,
    SetPasswordView,
)

urlpatterns = [
    path("register/", CreateAccountView.as_view(), name="api_register"),
    path("resend-otp/", SendOTPView.as_view(), name="api_resend_otp"),
    path("verify-email/", VerifyAccountEmailView.as_view(), name="api_verify_email"),
    path("login/", LoginView.as_view(), name="api_login"),
    path("verify-login/", VerifyLoginView.as_view(), name="api_verify_login"),
    path("set-password/", SetPasswordView.as_view(), name="api_set_password"),
    path("user-details/", UserDetailsView.as_view(), name="user_details"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete_account"),
]
