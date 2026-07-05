from django.db.models import QuerySet

from billing.models import OrderItemModel, OrderModel


class OrderItemRepository:
    """
    Order item database operations.
    """

    @staticmethod
    def create(**kwargs) -> OrderItemModel:
        return OrderItemModel.objects.create(**kwargs)

    @staticmethod
    def bulk_create(items: list[OrderItemModel]) -> list[OrderItemModel]:
        return OrderItemModel.objects.bulk_create(items)

    @staticmethod
    def get(item_id) -> OrderItemModel:
        return OrderItemModel.objects.select_related(
            "order",
            "product",
            "plan",
        ).get(id=item_id)

    @staticmethod
    def get_by_order(order: OrderModel) -> QuerySet[OrderItemModel]:
        return OrderItemModel.objects.select_related(
            "order",
            "product",
            "plan",
        ).filter(order=order)

    @staticmethod
    def delete(item: OrderItemModel) -> None:
        item.delete()
