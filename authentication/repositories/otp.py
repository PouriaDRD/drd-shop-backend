from django.db.models import F
from django.db import transaction

from authentication.models import OTPModel
from accounts.utils import normalize_iranian_mobile


class OTPRepository:
    """
    OTP database operations only.
    """

    @staticmethod
    @transaction.atomic
    def create_otp_code(phone_number: str, code: str, expires_at):
        """Create OTP record."""
        return OTPModel.objects.create(
            phone_number=normalize_iranian_mobile(phone_number),
            code=code,
            expires_at=expires_at,
        )

    @staticmethod
    def select_for_update(otp_id: str):
        return OTPModel.objects.select_for_update().filter(id=otp_id).first()

    @staticmethod
    def get_otp_by_id(otp_id: str):
        """Get OTP by ID."""
        return OTPModel.objects.filter(id=otp_id).first()

    @staticmethod
    def increment_attempts(otp: OTPModel):
        OTPModel.objects.filter(id=otp.id).update(attempts=otp.attempts + 1)

    @staticmethod
    def mark_verified(otp: OTPModel):
        OTPModel.objects.filter(id=otp.id).update(is_verified=True)
