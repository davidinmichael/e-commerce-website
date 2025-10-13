from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    FEMALE = "Female", _("Female")
    MALE = "Male", _("Male")
    OTHER = "Other", _("Other")


class UserType(models.TextChoices):
    USER = "User", _("User")
    AGENT = "Agent", _("Agent")
    ADMIN = "Admin", _("Admin")
    SUPER_ADMIN = "Super Admin", _("Super Admin")


class AccountStatus(models.TextChoices):
    SUSPENDED = "Suspended", _("Suspended")
    VERIFIED = "Verified", _("Verified")
    UNVERIFIED = "Unverified", _("Unverified")
    DEACTIVATED = "Deactivated", _("Deactivated")
