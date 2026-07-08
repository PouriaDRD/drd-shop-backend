from django.db import transaction

from accounts.models import ReferralProgramModel


class ReferralProgramRepository:
    """
    Repository for referral program settings.
    """

    @staticmethod
    def get_active() -> ReferralProgramModel | None:
        return ReferralProgramModel.objects.filter(
            is_enabled=True,
        ).first()

    @staticmethod
    @transaction.atomic
    def save(
        program: ReferralProgramModel,
        update_fields: list[str] | None = None,
    ):
        program.save(update_fields=update_fields)
        return program
