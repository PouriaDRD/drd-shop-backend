import logging
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from django.db.models import QuerySet

from accounts.models import UserModel
from shop.enums import OrderStatus, ProductType
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
    Service layer for handling order business logic.

    Responsibilities:
    - Creating orders from cart items
    - Approving/rejecting orders
    - Provisioning VPN services for VPN products
    """

    # =========================================================
    # ORDER CREATION
    # =========================================================

    @staticmethod
    @transaction.atomic
    def place_order(
        user: UserModel, cart_items: QuerySet[CartItemModel], total_price: int
    ) -> OrderModel:
        """
        Create a new order from cart items.

        Args:
            user (UserModel): The user placing the order.
            cart_items (QuerySet[CartItemModel]): Items in user's cart.
            total_price (int): Total calculated price of the cart.

        Returns:
            OrderModel: Created order instance.
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

    # =========================================================
    # ORDER APPROVAL
    # =========================================================

    @staticmethod
    @transaction.atomic
    def approve(order_id: str):
        """
        Approve an order and trigger provisioning if needed.

        Steps:
        - Lock order row
        - Ensure order is still pending
        - Mark order as approved
        - Create VPN subscriptions if required

        Args:
            order_id (str): Order UUID

        Returns:
            OrderModel: Updated order instance
        """

        order = OrderRepository.lock(order_id)

        if order.status != OrderStatus.PENDING:
            raise Exception("Order already processed.")

        OrderRepository.approve(order)

        items = OrderItemRepository.get_by_order(order)

        OrderService.create_vpn_subscription(items)

        logger.info(
            f"Order approved: id={order.id}, user={order.user}, total_price={order.total_price}",
        )

        return order

    # =========================================================
    # ORDER REJECTION
    # =========================================================

    @staticmethod
    @transaction.atomic
    def reject(order_id: str) -> OrderModel:
        """
        Reject an order.

        Args:
            order_id (str): Order UUID

        Returns:
            OrderModel: Rejected order instance
        """

        order = OrderRepository.lock(order_id)

        if order.status != OrderStatus.PENDING:
            raise Exception("Order already processed.")

        OrderRepository.reject(order)

        logger.info(
            f"Order rejected | id={order.id}, user={order.user}, total_price={order.total_price}",
        )

        return order

    # =========================================================
    # VPN PROVISIONING
    # =========================================================

    @staticmethod
    @transaction.atomic
    def create_vpn_subscription(order_items: QuerySet[OrderItemModel]):
        """
        Create VPN subscriptions for VPN products in an order.

        Each order item can generate multiple VPN services based on quantity.

        Rules:
        - Only products with type VPN are processed
        - Each unit of quantity creates one VPN service
        - Expiration is calculated based on plan "days" feature

        Args:
            order_items (QuerySet[OrderItemModel]): Order items

        Returns:
            list[VPNProvisionedServiceModel]: Created VPN services
        """

        vpn_objects: list[VPNProvisionedServiceModel] = []
        now = timezone.now()

        for item in order_items:
            if item.product.type != ProductType.VPN:
                continue

            days = OrderService.get_plan_days(item)
            expires_at = now + timedelta(days=days)

            vpn_objects.extend(
                [
                    VPNProvisionedServiceModel(
                        order_item=item,
                        subscription_link="",
                        content="",
                        expires_at=expires_at,
                    )
                    for _ in range(item.quantity)
                ]
            )

        VPNProvisionedServiceModel.objects.bulk_create(vpn_objects)

        logger.info(f"Subscriptions created: count={len(vpn_objects)}")

        return vpn_objects

    # =========================================================
    # PLAN HELPERS
    # =========================================================

    @staticmethod
    def get_plan_days(order_item: OrderItemModel) -> int:
        """
        Extract VPN duration (days) from plan features.

        Looks for feature with key "days".

        Args:
            order_item (OrderItemModel): Order item

        Returns:
            int: Duration in days (default: 30)
        """

        feature = order_item.plan.features.filter(  # type: ignore
            feature__key="days"
        ).first()

        if not feature:
            return 30

        return int(feature.value)
