from django.db import models
import uuid

from src.model_helpers import (
    KnowledgeBaseTypeOptions,
    QueryRequestStatusOptions,
    SourceOptions,
)


{
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
                {"name": "Haircut - Women", "price": 40, "duration_minutes": 45},
                {"name": "Haircut - Men", "price": 25, "duration_minutes": 30},
                {"name": "Hair Coloring", "price": 70, "duration_minutes": 90},
                {"name": "Hair Spa", "price": 60, "duration_minutes": 60},
            ],
        },
        {
            "category": "Skin",
            "items": [
                {"name": "Facial - Classic", "price": 50, "duration_minutes": 60},
                {"name": "Facial - Anti-aging", "price": 80, "duration_minutes": 75},
                {"name": "Threading - Eyebrows", "price": 10, "duration_minutes": 10},
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
                {"name": "Bridal Makeup", "price": 250, "duration_minutes": 180},
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


class User(models.Model):
    """
    Model representing a user.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class QueryRequest(models.Model):
    """
    Model representing a query request.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=1024)
    status = models.CharField(
        max_length=50,
        choices=QueryRequestStatusOptions.choices,
        default=QueryRequestStatusOptions.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:50]


class KnowledgeBase(models.Model):
    """
    Model representing a knowledge base.
    """
    question = models.CharField(blank=True, null=True, max_length=1024)
    answer = models.TextField()
    type = models.CharField(
        max_length=20,
        choices=KnowledgeBaseTypeOptions.choices,
        default=KnowledgeBaseTypeOptions.QUERY,
    )
    description = models.JSONField(blank=True, null=True)
    source = models.CharField(
        max_length=255, choices=SourceOptions.choices, default=SourceOptions.INITIAL
    )
    query_request = models.ForeignKey(
        QueryRequest, on_delete=models.CASCADE, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        """
        Override the save method to set the source to INITIAL if not provided.
        """
        if not self.question or not self.answer and self.type != KnowledgeBaseTypeOptions.INFO:
            raise ValueError("Question must be provided for query type.")
        
        if self.query_request and self.query_request.status != QueryRequestStatusOptions.RESOLVED:
            raise ValueError("Only resolved query requests can be linked to knowledge base entries.")

        super().save(*args, **kwargs)
