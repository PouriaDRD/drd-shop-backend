from django.db import transaction
from django.db.models import QuerySet

from accounts.models import UserModel
from shop.enums import OrderStatus
from shop.models import OrderModel


class OrderRepository:
    """
    Order database operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: UserModel,
        status: OrderStatus = OrderStatus.PENDING,
        total_price,
    ) -> OrderModel:
        return OrderModel.objects.create(
            user=user,
            status=status,
            total_price=total_price,
        )

    @staticmethod
    def get(user: UserModel) -> OrderModel | None:
        return (
            OrderModel.objects.prefetch_related(
                "items",
                "items__product",
                "items__plan",
            )
            .filter(user=user)
            .first()
        )

    @staticmethod
    def get_user_orders(user: UserModel) -> QuerySet[OrderModel]:
        return (
            OrderModel.objects.filter(user=user)
            .prefetch_related(
                "items__product",
                "items__plan__features__feature",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def save(order: OrderModel) -> OrderModel:
        order.save()
        return order

    @staticmethod
    @transaction.atomic
    def approve(order: OrderModel):
        order.status = OrderStatus.PAID
        order.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )
        return order

    @staticmethod
    @transaction.atomic
    def reject(order: OrderModel):
        order.status = OrderStatus.CANCELED
        order.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )
        return order

    @staticmethod
    def lock(order_id: str) -> OrderModel:
        return (
            OrderModel.objects.select_for_update()
            .prefetch_related(
                "items",
                "items__product",
                "items__plan",
                "items__plan__features__feature",
            )
            .get(id=order_id)
        )
