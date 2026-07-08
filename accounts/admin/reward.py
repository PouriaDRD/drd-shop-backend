from django.contrib import admin

from accounts.services import RewardService
from accounts.models import ReferralRewardModel


@admin.register(ReferralRewardModel)
class ReferralRewardAdmin(admin.ModelAdmin):

    list_display = (
        "inviter",
        "invited_user",
        "order",
        "order_amount_display",
        "commission_percent",
        "reward_amount_display",
        "status",
        "created_at",
    )

    search_fields = (
        "inviter__email",
        "invited_user__email",
        "order__id",
    )

    list_filter = (
        "status",
        "created_at",
    )

    readonly_fields = (
        "id",
        "inviter",
        "invited_user",
        "order",
        "order_amount",
        "commission_percent",
        "reward_amount",
        "created_at",
        "updated_at",
        "paid_at",
    )

    actions = [
        "process_pending_rewards",
    ]

    def order_amount_display(self, obj):

        return f"{obj.order_amount:,}"

    def reward_amount_display(self, obj):

        return f"{obj.reward_amount:,}"

    # ------------------------------------------
    # Manual approve
    # ------------------------------------------

    @admin.action(description="Process pending rewards")
    def process_pending_rewards(
        self,
        request,
        queryset,
    ):

        RewardService.process_pending_rewards()

        self.message_user(
            request,
            "Selected rewards processed.",
        )
