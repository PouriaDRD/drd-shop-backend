import logging
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.db.models import QuerySet

from accounts.models import UserModel

from shop.enums import OrderStatus
from shop.repositories.order import OrderRepository, OrderItemRepository
from shop.models import (
    OrderModel,
    OrderItemModel,
    CartItemModel,
    VPNProvisionedServiceModel,
)

logger = logging.getLogger("shop.order_service")


class OrderService:
    """
    Order business logic.
    """

    @staticmethod
    @transaction.atomic
    def place_order(
        user: UserModel, cart_items: QuerySet[CartItemModel], total_price: int
    ) -> OrderModel:
        """
        Create order.
        """

        order = OrderRepository.create(
            user=user,
            status=OrderStatus.PENDING,
            total_price=total_price,
        )

        order_items: list[OrderItemModel] = []

        for item in cart_items:
            order_items.append(
                OrderItemModel(
                    order=order,
                    product=item.product,
                    plan=item.plan,
                    quantity=item.quantity,
                    price=item.unit_price,
                )
            )

        OrderItemRepository.bulk_create(order_items)

        return order

    @staticmethod
    @transaction.atomic
    def approve(order_id: str):
        order = OrderRepository.lock(order_id)

        if order.status != OrderStatus.PENDING:
            raise Exception("Order already processed.")

        OrderRepository.approve(order)

        items = OrderItemRepository.get_by_order(order)

        vpn_objects = []

        for item in items:
            for _ in range(item.quantity):
                vpn_objects.append(
                    VPNProvisionedServiceModel(
                        order_item=item,
                        subscription_link="",
                        content="",
                        expires_at=timezone.now()
                        + timedelta(days=OrderService.get_plan_days(item)),
                    )
                )

        VPNProvisionedServiceModel.objects.bulk_create(vpn_objects)

        logger.info(
            f"Order approved: id={str(order.id)}, user={str(order.user)}, total_price={order.total_price}, vpn_created={len(vpn_objects)}",
        )

        return order

    @staticmethod
    @transaction.atomic
    def reject(order_id: str) -> OrderModel:
        """
        Reject order.
        """

        order = OrderRepository.lock(order_id)

        if order.status != OrderStatus.PENDING:
            raise Exception("Order already processed.")

        OrderRepository.reject(order)

        logger.info(
            f"Order rejected | id={str(order.id)}, user={str(order.user)}, total_price={order.total_price}",
        )

        return order

    @staticmethod
    def get_plan_days(order_item: OrderItemModel) -> int:
        feature = order_item.plan.features.filter(  # type: ignore
            feature__key="days"
        ).first()

        if not feature:
            return 30

        return int(feature.value)
