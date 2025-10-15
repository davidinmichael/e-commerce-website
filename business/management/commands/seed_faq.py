from django.core.management.base import BaseCommand

from business.models import FAQ
import os
from dotenv import load_dotenv
load_dotenv()

STORE_NAME = os.getenv("STORE_NAME", "Online Store")
SHOP_EMAIL = os.getenv("SHOP_EMAIL", "info@onlinestore.com")
class Command(BaseCommand):
    help = "Seeds default Frequently Asked Questions (FAQs) for RestInn."

    def handle(self, *args, **options):
        faqs = [
            {
                "question": f"What is {STORE_NAME}?",
                "answer": (
                    f"{STORE_NAME} is your one-stop online store for the latest smartphones, laptops, accessories, "
                    "and other electronic gadgets — all sourced from trusted brands and verified sellers."
                ),
            },
            {
                "question": "Do I need an account to buy gadgets?",
                "answer": (
                    "You can browse and explore products without an account. "
                    "Follow the on-screen instructions to complete your order securely."
                ),
            },
            {
                "question": "How do I place an order?",
                "answer": (
                    "Simply select the gadget you want, click 'Add to Cart', and proceed to checkout. "
                    "Follow the on-screen instructions to complete your order securely."
                ),
            },
            {
                "question": "What payment options are available?",
                "answer": (
                    "We accept multiple payment methods including debit/credit cards, bank transfers, and cash on delivery "
                    "(available in select locations)."
                ),
            },
            {
                "question": "Do you offer delivery services?",
                "answer": (
                    "Yes. We deliver nationwide through our trusted logistics partners. "
                    "Delivery timelines vary depending on your location, but most orders arrive within 2–5 business days."
                ),
            },
            {
                "question": "Can I return or exchange an item?",
                "answer": (
                    "Yes. Items can be returned or exchanged within 7 days of delivery if they are unused, "
                    "in original packaging, and meet our return policy terms."
                ),
            },
            {
                "question": "Are your products genuine?",
                "answer": (
                    "Absolutely. All products sold on GadgetHub are 100% original and sourced directly from "
                    "authorized distributors or verified sellers."
                ),
            },
            {
                "question": "Do you offer warranty on products?",
                "answer": (
                    "Yes. Most of our gadgets come with the manufacturer’s warranty. "
                    "Warranty duration and coverage vary depending on the brand and product type."
                ),
            },
            {
                "question": "Who do I contact for support?",
                "answer": (
                    "Our support team is available to assist you with any inquiries. "
                    "You can reach us through the Contact Us page, via WhatsApp, or by emailing support@gadgethub.com."
                ),
            },
        ]

        FAQ.objects.all().delete()

        created_count = 0
        for faq in faqs:
            obj, created = FAQ.objects.get_or_create(**faq)
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{created_count} FAQ entries successfully created or already exist."
            )
        )
