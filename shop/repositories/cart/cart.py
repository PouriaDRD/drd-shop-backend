from django.db import transaction

from shop.models import CartModel


class CartRepository:
    """
    Cart DB operations.
    """

    @staticmethod
    @transaction.atomic
    def get_or_create(user):
        cart, created = CartModel.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def get(user):
        return (
            CartModel.objects.select_related("coupon")
            .prefetch_related("items", "items__product", "items__plan")
            .filter(user=user)
            .first()
        )

    @staticmethod
    @transaction.atomic
    def save(cart: CartModel):
        cart.save()
        return cart
