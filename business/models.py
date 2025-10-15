from unittest.mock import Base

from django.db import models
from django.utils.text import slugify

from account.models import Account
from core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)


class Product(BaseModel):
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.JSONField(default=list, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    features = models.JSONField(default=list)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Discount percentage (e.g. 10 for 10%)",
    )
    images = models.JSONField(default=list, blank=True)
    featured_image = models.URLField()
    inventory_count = models.PositiveIntegerField(default=0, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.inventory_count}"

    class Meta:
        ordering = ["-id"]

    @property
    def discounted_price(self):
        """Return price after applying discount."""
        if self.discount > 0:
            return self.price - (self.price * (self.discount / 100))
        return self.price

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided."""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class FAQ(BaseModel):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
