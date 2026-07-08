from django.db import transaction
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from accounts.models import UserModel

from billing.services.order import OrderService
from billing.repositories.cart import CartRepository
from billing.models import CartItemModel, OrderModel


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

        order = OrderService.place_order(
            user=user,
            cart_items=items,
            total_price=cart.total_price,
            coupon=cart.coupon,
            discount_amount=cart.discount,
            subtotal=cart.subtotal,
        )

        from finance.services.purchase import PurchaseService

        PurchaseService.create(
            wallet=wallet,
            amount=cart.total_price,
            reason=f"خرید #{str(order.id)[:8]}",  # type: ignore
            order=order,
        )

        # reset cart
        items.delete()
        CartRepository.reset_cart(cart)

        return order
