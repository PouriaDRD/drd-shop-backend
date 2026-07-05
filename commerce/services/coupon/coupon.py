from django.db.models import Sum
from django.utils import timezone
from django.db import models, transaction

from billing.models import OrderModel
from commerce.enums import DiscountType
from finance.models import WalletModel
from commerce.models import CouponModel, CouponUsageModel


class CouponService:
    """
    Coupon business logic (production-safe version).
    """

    @staticmethod
    def calculate_discount(
        coupon: CouponModel,
        subtotal: int,
        *,
        user_id=None,
        product_ids=None,
    ) -> int:
        now = timezone.now()

        if not coupon or not coupon.is_active:
            return 0

        if coupon.starts_at and coupon.starts_at > now:
            return 0

        if coupon.expires_at and coupon.expires_at < now:
            return 0

        if subtotal < coupon.minimum_order_amount:
            return 0

        # usage limit check (global)
        if coupon.usage_limit is not None:
            if coupon.usages.count() >= coupon.usage_limit:  # type: ignore
                return 0

        # per user limit check
        if user_id and coupon.per_user_limit:
            user_usage_count = coupon.usages.filter(wallet__user_id=user_id).count()  # type: ignore
            if user_usage_count >= coupon.per_user_limit:
                return 0

        # product restriction check
        if coupon.allowed_products.exists() and product_ids:
            allowed_ids = set(coupon.allowed_products.values_list("id", flat=True))
            if not set(product_ids).intersection(allowed_ids):
                return 0

        # calculate discount
        if coupon.discount_type == DiscountType.PERCENT:
            percent = max(0, min(coupon.discount_value, 100))
            discount = (subtotal * percent) // 100
        else:
            discount = coupon.discount_value

        # max cap
        if coupon.max_discount:
            discount = min(discount, coupon.max_discount)

        # never exceed subtotal
        return max(0, min(discount, subtotal))

    @staticmethod
    @transaction.atomic
    def apply_coupon(
        *,
        coupon: CouponModel,
        wallet: WalletModel,
        order: OrderModel,
        discount: int,
    ):
        """
        This should be called ONLY after:
        - order is created
        - discount is confirmed
        """

        if discount <= 0:
            return None

        # extra safety check (never trust upstream)
        if not coupon.is_active:
            return None

        usage = CouponUsageModel.objects.create(
            coupon=coupon,
            wallet=wallet,
            order=order,
            discount_amount=discount,
        )

        # optional: keep counter in sync (if you keep used_count)
        CouponModel.objects.filter(id=coupon.id).update(
            used_count=models.F("used_count") + 1
        )

        return usage
