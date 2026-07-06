from django.db import models


class EmailStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SENT = "sent", "Sent"
    FAILED = "failed", "Failed"


class TemplateType(models.TextChoices):
    CUSTOM = "custom", "Custom Template"
    PREDEFINED = "predefined", "Predefined Template"
