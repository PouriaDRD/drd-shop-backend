from django.contrib import admin

from accounts.models import ReferralProgramModel


@admin.register(ReferralProgramModel)
class ReferralProgramAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "commission_percent",
        "minimum_order_amount",
        "maximum_reward_amount",
        "reward_delay_days",
        "is_enabled",
        "created_at",
    )

    list_filter = (
        "is_enabled",
        "created_at",
    )

    search_fields = ("name",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    actions = [
        "activate_program",
        "deactivate_program",
    ]

    @admin.action(description="Activate selected programs")
    def activate_program(
        self,
        request,
        queryset,
    ):

        queryset.update(
            is_active=True,
        )

        self.message_user(
            request,
            "Selected programs activated.",
        )

    @admin.action(description="Deactivate selected programs")
    def deactivate_program(
        self,
        request,
        queryset,
    ):

        queryset.update(
            is_active=False,
        )

        self.message_user(
            request,
            "Selected programs deactivated.",
        )
