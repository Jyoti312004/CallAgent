from django.db import models
import uuid

from src.model_helpers import (
    KnowledgeBaseTypeOptions,
    QueryRequestStatusOptions,
    SourceOptions,
)

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
