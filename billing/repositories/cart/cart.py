from django.db import transaction

from billing.models import CartModel
from accounts.models import UserModel


class CartRepository:
    """
    Cart database operations.
    """

    @staticmethod
    @transaction.atomic
    def get_or_create(user: UserModel):
        cart, created = CartModel.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def get(user: UserModel) -> CartModel | None:
        return (
            CartModel.objects.select_related("coupon")
            .prefetch_related(
                "items",
                "items__product",
                "items__plan",
            )
            .filter(user=user)
            .first()
        )

    @staticmethod
    @transaction.atomic
    def save(cart: CartModel) -> CartModel:
        cart.save(
            update_fields=[
                "coupon",
                "subtotal",
                "discount",
                "total_price",
            ]
        )
        return cart

    @staticmethod
    @transaction.atomic
    def reset_cart(cart: CartModel) -> CartModel:
        cart.coupon = None
        cart.subtotal = 0
        cart.discount = 0
        cart.total_price = 0

        return CartRepository.save(cart)
