import random

from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from core.utils import generate_random_code

from .choices import AccountStatus, Gender, UserType


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        else:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            if password:
                user.set_password(password)
            user.is_active = True
            user.save(using=self._db)
            return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractUser):
    first_name = models.CharField(max_length=50, null=True, blank=True, default="User")
    last_name = models.CharField(
        max_length=50, null=True, blank=True, default="Account"
    )
    email = models.EmailField(unique=True, verbose_name="email address")
    phone_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    password = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=10,
    )
    profile_image = models.URLField(blank=True, null=True)
    user_type = models.CharField(
        max_length=50, choices=UserType.choices, default=UserType.USER
    )
    account_status = models.CharField(
        max_length=50, choices=AccountStatus.choices, default=AccountStatus.UNVERIFIED
    )
    otp_token = models.CharField(max_length=6, null=True, blank=True, unique=True)
    is_2fa_enabled = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_admin_user = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    username = models.CharField(max_length=150, blank=True, null=True, unique=True)

    USERNAME_FIELD = "email"
    objects = AccountManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.otp_token:
            self.otp_token = generate_random_code()
        if not self.username:
            base = slugify(self.first_name or "user")
            unique = f"{base}-{random.randint(100, 999999)}"
            while Account.objects.filter(username=unique).exists():
                unique = f"{base}-{random.randint(100, 999999)}"
                self.username = unique
        return super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class AccountDeleteRequest(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    date_requested = models.DateField(auto_now=True)
