from django.db import transaction

from billing.models import CartItemModel


class CartItemRepository:
    """
    Cart item DB operations.
    """

    @staticmethod
    @transaction.atomic
    def create(**kwargs) -> CartItemModel:
        return CartItemModel.objects.create(**kwargs)

    @staticmethod
    def get(item_id) -> CartItemModel:
        return CartItemModel.objects.select_related(
            "cart",
            "product",
            "plan",
        ).get(id=item_id)

    @staticmethod
    @transaction.atomic
    def delete(item: CartItemModel):
        item.delete()
