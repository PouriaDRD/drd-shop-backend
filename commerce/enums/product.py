from django.db import models


class ProductType(models.TextChoices):
    VPN = "vpn", "VPN"
    GAME = "game", "Game"
    GIFT_CARD = "gift_card", "Gift Card"
    OTHER = "other", "Other"
