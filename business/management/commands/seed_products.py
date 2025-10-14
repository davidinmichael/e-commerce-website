from django.core.management.base import BaseCommand
from django.utils.text import slugify
from decimal import Decimal
import random

from business.models import Product, Category


class Command(BaseCommand):
    help = "Seed the database with sample products"

    def handle(self, *args, **options):
        categories_data = {
            "Phones": "https://res.cloudinary.com/dskpdlvxu/image/upload/v1760454122/iPhone_d1a1q9.jpg",
            "Computers": "https://res.cloudinary.com/dskpdlvxu/image/upload/v1760454333/computer_qv17ad.jpg",
            "Smart Watch": "https://res.cloudinary.com/dskpdlvxu/image/upload/v1760454087/smart_watch_mdlhmu.jpg",
            "AirPods": "https://res.cloudinary.com/dskpdlvxu/image/upload/v1760454315/airpod_qq77jz.jpg",
            "Games": "https://res.cloudinary.com/dskpdlvxu/image/upload/v1760454117/game_j4nn0y.jpg",
        }

        # Optional: clear old seeded data
        Product.objects.all().delete()

        for category_name, image_url in categories_data.items():
            try:
                category = Category.objects.get(name__iexact=category_name)
            except Category.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"Category '{category_name}' not found, skipping..."
                    )
                )
                continue

            # Seed multiple products per category
            for i in range(3):
                title = f"{category_name} Model {i + 1}"
                slug = slugify(title)
                price = Decimal(random.randint(200, 2000))
                discount = Decimal(random.choice([0, 5, 10, 15]))
                inventory_count = random.randint(5, 50)
                tags = [category_name.lower(), "gadget", "electronics"]
                features = [
                    "Durable design",
                    "High performance",
                    "1-year warranty",
                ]

                product = Product.objects.create(
                    created_by=None,  # Leave blank for now
                    title=title,
                    slug=slug,
                    description=f"This is a premium {category_name.lower()} designed for high performance.",
                    price=price,
                    discount=discount,
                    category=category,
                    tags=tags,
                    features=features,
                    images=[image_url],
                    featured_image=image_url,
                    inventory_count=inventory_count,
                    is_published=True,
                )

                self.stdout.write(self.style.SUCCESS(f"Added: {product.title}"))

        self.stdout.write(self.style.SUCCESS("✅ Product seeding complete."))
