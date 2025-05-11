from django.core.management.base import BaseCommand
from django.db import transaction
from src.models import KnowledgeBase
from src.model_helpers import SourceOptions, KnowledgeBaseTypeOptions


class Command(BaseCommand):
    help = "Populates the database with salon information"

    def handle(self, *args, **kwargs):
        try:
            self.import_salon_data()
            self.stdout.write(self.style.SUCCESS("Salon data imported successfully"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing salon data: {str(e)}"))

    @transaction.atomic
    def import_salon_data(self):
        salon_data = {
            "salon_info": {
                "name": "Glamora Salon & Spa",
                "address": "123 Radiant Ave, Downtown Cityville, CA 90210",
                "phone": "+1-555-123-4567",
                "email": "info@glamorasalon.com",
                "working_hours": {
                    "monday_to_friday": "10:00 AM - 8:00 PM",
                    "saturday": "9:00 AM - 6:00 PM",
                    "sunday": "Closed",
                },
                "social_media": {
                    "instagram": "https://instagram.com/glamorasalon",
                    "facebook": "https://facebook.com/glamorasalon",
                },
            },
            "services": [
                {
                    "category": "Hair",
                    "items": [
                        {
                            "name": "Haircut - Women",
                            "price": 40,
                            "duration_minutes": 45,
                        },
                        {"name": "Haircut - Men", "price": 25, "duration_minutes": 30},
                        {"name": "Hair Coloring", "price": 70, "duration_minutes": 90},
                        {"name": "Hair Spa", "price": 60, "duration_minutes": 60},
                    ],
                },
                {
                    "category": "Skin",
                    "items": [
                        {
                            "name": "Facial - Classic",
                            "price": 50,
                            "duration_minutes": 60,
                        },
                        {
                            "name": "Facial - Anti-aging",
                            "price": 80,
                            "duration_minutes": 75,
                        },
                        {
                            "name": "Threading - Eyebrows",
                            "price": 10,
                            "duration_minutes": 10,
                        },
                    ],
                },
                {
                    "category": "Nails",
                    "items": [
                        {"name": "Manicure", "price": 30, "duration_minutes": 40},
                        {"name": "Pedicure", "price": 35, "duration_minutes": 45},
                        {"name": "Nail Art", "price": 25, "duration_minutes": 30},
                    ],
                },
                {
                    "category": "Makeup",
                    "items": [
                        {"name": "Party Makeup", "price": 100, "duration_minutes": 90},
                        {
                            "name": "Bridal Makeup",
                            "price": 250,
                            "duration_minutes": 180,
                        },
                    ],
                },
            ],
            "staff": [
                {
                    "id": 1,
                    "name": "Sophia Blake",
                    "role": "Senior Hair Stylist",
                    "experience_years": 8,
                    "specialization": ["Haircut", "Hair Spa", "Hair Coloring"],
                },
                {
                    "id": 2,
                    "name": "Liam Carter",
                    "role": "Skin Specialist",
                    "experience_years": 5,
                    "specialization": ["Facials", "Threading"],
                },
                {
                    "id": 3,
                    "name": "Ava Chen",
                    "role": "Nail Artist",
                    "experience_years": 4,
                    "specialization": ["Nail Art", "Manicure", "Pedicure"],
                },
                {
                    "id": 4,
                    "name": "Emma Rodriguez",
                    "role": "Makeup Artist",
                    "experience_years": 7,
                    "specialization": ["Bridal Makeup", "Party Makeup"],
                },
            ],
            "policies": {
                "cancellation": "Cancellations must be made at least 24 hours in advance. Late cancellations may be subject to a 50% charge.",
                "booking": "Advance booking is recommended. Walk-ins are accepted based on availability.",
                "payments": ["Cash", "Credit Card", "Mobile Wallets"],
                "safety": "All tools are sanitized after every use. Masks are optional but recommended.",
            },
        }

        # Create INFO type entries
        KnowledgeBase.objects.create(
            type=KnowledgeBaseTypeOptions.INFO,
            description={"salon_info": salon_data["salon_info"]},
            source=SourceOptions.INITIAL,
        )

        KnowledgeBase.objects.create(
            type=KnowledgeBaseTypeOptions.INFO,
            description={"services": salon_data["services"]},
            source=SourceOptions.INITIAL,
        )

        KnowledgeBase.objects.create(
            type=KnowledgeBaseTypeOptions.INFO,
            description={"staff": salon_data["staff"]},
            source=SourceOptions.INITIAL,
        )

        KnowledgeBase.objects.create(
            type=KnowledgeBaseTypeOptions.INFO,
            description={"policies": salon_data["policies"]},
            source=SourceOptions.INITIAL,
        )

        # Create QUERY type entries (common questions)
        KnowledgeBase.objects.create(
            type=KnowledgeBaseTypeOptions.QUERY,
            question="What are the salon's working hours?",
            answer=f"Monday to Friday: {salon_data['salon_info']['working_hours']['monday_to_friday']}, "
            f"Saturday: {salon_data['salon_info']['working_hours']['saturday']}, "
            f"Sunday: {salon_data['salon_info']['working_hours']['sunday']}",
            description={
                "topic": "working_hours",
                "data": salon_data["salon_info"]["working_hours"],
            },
            source=SourceOptions.INITIAL,
        )

        # Add more common questions for better coverage
        KnowledgeBase.objects.create(
            type=KnowledgeBaseTypeOptions.QUERY,
            question="What services do you offer?",
            answer="We offer various services in categories including Hair, Skin, Nails, and Makeup. "
            "Our hair services include women's and men's haircuts, coloring, and hair spa treatments. "
            "For skin, we provide classic and anti-aging facials and eyebrow threading. "
            "Our nail services include manicures, pedicures, and nail art. "
            "We also offer party and bridal makeup services.",
            description={"topic": "services", "data": salon_data["services"]},
            source=SourceOptions.INITIAL,
        )

        KnowledgeBase.objects.create(
            type=KnowledgeBaseTypeOptions.QUERY,
            question="What is your cancellation policy?",
            answer=salon_data["policies"]["cancellation"],
            description={
                "topic": "cancellation_policy",
                "data": salon_data["policies"]["cancellation"],
            },
            source=SourceOptions.INITIAL,
        )

        KnowledgeBase.objects.create(
            type=KnowledgeBaseTypeOptions.QUERY,
            question="How can I book an appointment?",
            answer=salon_data["policies"]["booking"],
            description={
                "topic": "booking_policy",
                "data": salon_data["policies"]["booking"],
            },
            source=SourceOptions.INITIAL,
        )

        self.stdout.write(
            "Added salon information and common questions to knowledge base"
        )
