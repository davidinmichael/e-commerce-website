from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views import View

from account.choices import UserType
from account.forms import AccountForm, LoginForm
from account.models import Account


class RegisterAdminView(View):

    def get(self, request):
        return render(request, "admin_app/register.html")

    def post(self, request):
        form = AccountForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user = form.save(commit=False)
            user.set_password(password)
            user.user_type = UserType.ADMIN
            user.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("dashboard")
        messages.error(request, "Incorrect form details!")
        return render(request, "admin_app/register.html")


class LoginAdminView(View):

    def get(self, request):
        return render(request, "admin_app/login.html")

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                messages.warning(request, "Invalid email or password!")
                return render(request, "admin_app/login.html")

            if user.check_password(password):
                login(request, user)
                return redirect("dashboard")
            messages.error(request, "Incorrect login details!")

        return render(request, "admin_app/login.html")


def logout_view(request):
    logout(request)
    return redirect("login_admin")


class DashboardView(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "You don't have permission to access this page.")
            return redirect("login_admin")
        return render(request, "admin_app/dashboard.html")
