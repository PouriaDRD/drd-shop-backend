from django.db import transaction
from django.db.models import Sum

from accounts.enums import RewardStatus
from accounts.models import ReferralRewardModel


class ReferralRewardRepository:

    @staticmethod
    @transaction.atomic
    def create(
        **kwargs,
    ):

        return ReferralRewardModel.objects.create(
            **kwargs,
        )

    @staticmethod
    def get_by_id(reward_id):

        return (
            ReferralRewardModel.objects.select_related(
                "inviter",
                "invited_user",
                "order",
            )
            .filter(
                id=reward_id,
            )
            .first()
        )

    @staticmethod
    def get_user_rewards(user):

        return (
            ReferralRewardModel.objects.filter(
                inviter=user,
            )
            .select_related(
                "invited_user",
                "order",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def get_pending():

        return ReferralRewardModel.objects.filter(
            status=RewardStatus.PENDING,
        )

    @staticmethod
    @transaction.atomic
    def approve(reward):

        reward.status = RewardStatus.APPROVED

        reward.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return reward

    @staticmethod
    @transaction.atomic
    def reject(reward):

        reward.status = RewardStatus.REJECTED

        reward.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return reward

    @staticmethod
    @transaction.atomic
    def paid(
        reward,
        transaction_obj,
    ):

        reward.status = RewardStatus.PAID
        reward.transaction = transaction_obj

        reward.save(
            update_fields=[
                "status",
                "transaction",
                "paid_at",
                "updated_at",
            ]
        )

        return reward

    @staticmethod
    def total_paid(user):

        return (
            ReferralRewardModel.objects.filter(
                inviter=user,
                status=RewardStatus.PAID,
            ).aggregate(total=Sum("reward_amount"),)["total"]
            or 0
        )

    @staticmethod
    def total_pending(user):

        return (
            ReferralRewardModel.objects.filter(
                inviter=user,
                status=RewardStatus.PENDING,
            ).aggregate(total=Sum("reward_amount"),)["total"]
            or 0
        )
