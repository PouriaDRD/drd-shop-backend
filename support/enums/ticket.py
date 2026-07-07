from django.db import models


class TicketStatus(models.TextChoices):

    OPEN = (
        "open",
        "Open",
    )

    ANSWERED = (
        "answered",
        "Answered",
    )

    CLOSED = (
        "closed",
        "Closed",
    )


class TicketPriority(models.TextChoices):

    LOW = (
        "low",
        "Low",
    )

    MEDIUM = (
        "medium",
        "Medium",
    )

    HIGH = (
        "high",
        "High",
    )


class TicketCategory(models.TextChoices):

    GENERAL = (
        "general",
        "General",
    )

    PAYMENT = (
        "payment",
        "Payment",
    )

    ORDER = (
        "order",
        "Order",
    )

    TECHNICAL = (
        "technical",
        "Technical",
    )
