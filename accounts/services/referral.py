import string
import secrets
from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError

from accounts.models import UserModel
from accounts.enums import RewardStatus
from accounts.repositories import (
    ReferralCodeRepository,
    ReferralProgramRepository,
    ReferralRewardRepository,
)

from billing.models import OrderModel


class ReferralService:
    """
    Referral business logic.
    """

    @staticmethod
    @transaction.atomic
    def create_referral_code(user: UserModel):
        """
        Create referral code for user.
        """

        referral = ReferralCodeRepository.get_by_user(user)

        if referral:
            return referral

        code = ReferralCodeGenerator.generate()

        return ReferralCodeRepository.create(
            user=user,
            code=code,
        )

    @staticmethod
    @transaction.atomic
    def apply_referral_code(
        *,
        user: UserModel,
        code: str,
    ):
        """
        Attach inviter to newly registered user.
        """

        referral = ReferralCodeRepository.get_by_code(code)

        if referral is None:
            raise ValidationError("Referral code not found.", code="invalid_code")

        if referral.user.id == user.id:
            raise ValidationError(
                "You cannot use your own referral code.", code="invalid_code"
            )

        if user.referred_by:
            raise ValidationError("Referral already applied.", code="invalid_code")

        user.referred_by = referral.user  # type: ignore
        user.save(update_fields=["referred_by"])

        ReferralCodeRepository.increase_signups(referral)

        return referral

    @staticmethod
    @transaction.atomic
    def create_reward(
        *,
        order: OrderModel,
    ):
        """
        Create reward after order approval.
        """

        user = order.user

        if not user.referred_by:
            return None

        program = ReferralProgramRepository.get_active()

        if not program:
            return None

        if order.total_price < program.minimum_order_amount:
            return None

        reward_amount = int(
            Decimal(order.total_price) * program.commission_percent / Decimal("100")
        )

        if (
            program.maximum_reward_amount
            and reward_amount > program.maximum_reward_amount
        ):
            reward_amount = program.maximum_reward_amount

        reward = ReferralRewardRepository.create(
            inviter=user.referred_by,
            invited_user=user,
            order=order,
            order_amount=order.total_price,
            commission_percent=program.commission_percent,
            reward_amount=reward_amount,
            status=RewardStatus.PENDING,
        )

        referral = ReferralCodeRepository.get_by_user(user.referred_by)

        if referral:
            ReferralCodeRepository.increase_orders(referral)
            ReferralCodeRepository.add_earned(
                referral,
                reward_amount,
            )

        return reward


class ReferralCodeGenerator:
    """
    Generate unique referral codes.
    """

    LENGTH = 6

    CHARS = string.ascii_uppercase + string.digits

    @classmethod
    def generate(cls) -> str:
        while True:
            code = "".join(secrets.choice(cls.CHARS) for _ in range(cls.LENGTH))

            if not ReferralCodeRepository.get_by_code(code):
                return f"DRD-{code}"
