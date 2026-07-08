from django.db import transaction
from django.db.models import F

from accounts.models import ReferralCodeModel


class ReferralCodeRepository:

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user,
        code: str,
    ):

        return ReferralCodeModel.objects.create(
            user=user,
            code=code,
        )

    @staticmethod
    def get_by_code(
        code: str,
    ) -> ReferralCodeModel | None:

        return (
            ReferralCodeModel.objects.select_related(
                "user",
            )
            .filter(
                code=code,
                is_active=True,
            )
            .first()
        )

    @staticmethod
    def get_by_user(user):

        return ReferralCodeModel.objects.filter(
            user=user,
        ).first()

    @staticmethod
    @transaction.atomic
    def increase_clicks(referral):

        referral.clicks = F("clicks") + 1
        referral.save(update_fields=["clicks"])

    @staticmethod
    @transaction.atomic
    def increase_signups(referral):

        referral.signups = F("signups") + 1
        referral.save(update_fields=["signups"])

    @staticmethod
    @transaction.atomic
    def increase_orders(referral):

        referral.orders = F("orders") + 1
        referral.save(update_fields=["orders"])

    @staticmethod
    @transaction.atomic
    def add_earned(
        referral,
        amount: int,
    ):

        referral.total_earned = F("total_earned") + amount

        referral.save(
            update_fields=["total_earned"],
        )

    @staticmethod
    @transaction.atomic
    def add_paid(
        referral,
        amount: int,
    ):

        referral.total_paid = F("total_paid") + amount

        referral.save(
            update_fields=["total_paid"],
        )
