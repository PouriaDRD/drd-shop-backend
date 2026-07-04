from django.db import transaction
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from accounts.models import UserModel
from finance.services import PurchaseService

from shop.enums import OrderStatus
from shop.repositories.cart import CartRepository
from shop.models import CartItemModel, OrderItemModel, OrderModel
from shop.repositories.order import OrderItemRepository, OrderRepository


class CheckoutService:
    """
    Convert cart into order.
    """

    @staticmethod
    @transaction.atomic
    def checkout(user: UserModel) -> OrderModel:
        """
        Convert cart into order.
        """

        cart = CartRepository.get(user)

        if cart is None:
            raise ValidationError("سبد خرید خالی است")

        items: QuerySet[CartItemModel] = cart.items.select_related(  # type: ignore
            "product",
            "plan",
        )

        if not items.exists():
            raise ValidationError("سبد خرید خالی است")

        wallet = getattr(user, "wallet", None)

        if wallet is None:
            raise ValidationError("کیف پول وجود ندارد")

        if wallet.balance < cart.total_price:
            raise ValidationError("موجودی کافی نیست")

        order = OrderRepository.create(
            user=user,
            status=OrderStatus.PENDING,
            total_price=cart.total_price,
        )

        order_items: list[OrderItemModel] = []

        for item in items:
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

        PurchaseService.create(
            wallet=wallet,
            amount=cart.total_price,
            reason="خرید محصول",
        )

        # reset cart
        items.delete()

        cart.coupon = None
        cart.subtotal = 0
        cart.discount = 0
        cart.total_price = 0

        CartRepository.save(cart)

        return order
