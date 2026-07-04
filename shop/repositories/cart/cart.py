from django.db.models import QuerySet

from accounts.models import UserModel
from shop.models import CartModel


class CartRepository:
    """
    Cart database operations.
    """

    @staticmethod
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
