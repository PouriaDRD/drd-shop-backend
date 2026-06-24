from typing import Optional
from django.utils import timezone
from authentication.models import OTPModel

from config.settings.app_config import config


class OTPSelector:
    """
    Read-only helper for otp state checks.
    """

    MAX_OTP_ATTEMPTS = config.auth.max_otp_attempts

    @staticmethod
    def is_expired(otp: Optional[OTPModel]) -> bool:
        if not otp:
            return False
        return timezone.now() > otp.expires_at

    @staticmethod
    def is_verified(otp: Optional[OTPModel]) -> bool:
        if not otp:
            return False
        return otp.is_verified

    @classmethod
    def remaining_attempts(cls, otp: Optional[OTPModel]) -> int:
        if not otp:
            return 0

        return max(0, cls.MAX_OTP_ATTEMPTS - otp.attempts)
