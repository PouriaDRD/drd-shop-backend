from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from accounts.repositories import (
    ReferralProgramRepository,
    ReferralRewardRepository,
    ReferralCodeRepository,
)

from billing.enums import OrderStatus
from finance.enums import TransactionType
from finance.services import TransactionService, LedgerService

from notifications.services import NotificationService


class RewardService:

    @staticmethod
    @transaction.atomic
    def process_pending_rewards():

        program = ReferralProgramRepository.get_active()

        if not program:
            return 0

        before = timezone.now() - timedelta(days=program.reward_delay_days)

        rewards = (
            ReferralRewardRepository.get_pending()
            .filter(created_at__lte=before)
            .select_related(
                "inviter",
            )
        )

        processed = 0

        for reward in rewards:
            if reward.order.status != OrderStatus.PAID:
                continue

            transaction = TransactionService.create(
                wallet=reward.inviter.wallet,  # type: ignore
                amount=reward.reward_amount,
                transaction_type=TransactionType.REFERRAL_REWARD,
                description=f"پاداش سفارش موفق {reward.invited_user}",
            )

            TransactionService.approve(str(transaction.id))

            LedgerService.create(
                wallet=reward.inviter.wallet,  # type: ignore
                transaction=transaction,
                transaction_type=TransactionType.REFERRAL_REWARD,
                amount=reward.reward_amount,
            )

            ReferralRewardRepository.paid(
                reward,
                transaction,
            )

            NotificationService.create_success(
                user=reward.inviter,
                title="پاداش معرفی واریز شد",
                message=f"{reward.reward_amount:,} تومان به کیف پول شما اضافه شد.",
            )

            referral = ReferralCodeRepository.get_by_user(reward.inviter)

            if referral:
                ReferralCodeRepository.add_paid(
                    referral,
                    reward.reward_amount,
                )

            processed += 1

        return processed
