# src/tasks.py

from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import QueryRequest, QueryRequestStatusOptions
import logging
logger = logging.getLogger(__name__)

@shared_task
def mark_unresolved_if_expired():
    two_hours_ago = timezone.now() - timedelta(hours=2)
    queries = QueryRequest.objects.filter(status=QueryRequestStatusOptions.PENDING, updated_at__lte=two_hours_ago)

    updated_count = queries.update(status=QueryRequestStatusOptions.UNRESOLVED)

    logger.info(f'Marked {updated_count} queries as unresolved.')
    return f'Marked {updated_count} queries as unresolved.'

