

from django.db import models

class SourceOptions(models.TextChoices):
    INITIAL = 'initial', 'Initial'
    SUPERVISOR = 'supervisor', 'Supervisor'

class QueryRequestStatusOptions(models.TextChoices):
    PENDING = 'pending', 'Pending'
    RESOLVED = 'resolved', 'Resolved'
    UNRESOLVED = 'unresolved', 'Unresolved'

class KnowledgeBaseTypeOptions(models.TextChoices):
    QUERY = 'query', 'Query'
    INFO = 'info', 'Info'