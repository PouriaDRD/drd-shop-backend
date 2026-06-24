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
    def get_otp_by_id(otp_id: str):
        """Get OTP by ID."""
        return OTPModel.objects.filter(id=otp_id).first()

    @staticmethod
    def increment_attempts(otp: OTPModel):
        """
        Safe increment attempts (race-condition safe).
        """
        OTPModel.objects.filter(id=otp.id).update(attempts=F("attempts") + 1)
        otp.refresh_from_db()
        return otp

    @staticmethod
    def mark_as_verified(otp: OTPModel):
        """Mark OTP as verified."""
        otp.is_verified = True
        otp.save(update_fields=["is_verified"])
        return otp
