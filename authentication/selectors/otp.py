import hmac
import hashlib
from typing import Optional
from django.utils import timezone
from datetime import datetime, timedelta

from authentication.models import OTPModel
from config.settings.app_config import config


class OTPSelector:
    """Selector class for OTP-related properties."""

    OTP_LENGTH = config.auth.otp_length
    OTP_TTL_MINUTES = config.auth.otp_ttl_minutes
    MAX_OTP_ATTEMPTS = config.auth.max_otp_attempts

    @staticmethod
    def is_expired(otp: Optional[OTPModel]) -> bool:
        """Check if OTP is expired by comparing current time with expire_at."""
        if not otp:
            return True
        now = timezone.now()
        expire_at = OTPSelector.expire_at(otp)
        result = now > expire_at
        return result

    @staticmethod
    def expire_at(otp: OTPModel) -> datetime:
        """Return datetime object for expiry of OTP."""
        result = otp.created_at + timedelta(minutes=OTPSelector.OTP_TTL_MINUTES)
        return result

    @staticmethod
    def is_used(otp: OTPModel) -> bool:
        """Check if OTP is used."""
        return otp.is_used

    @staticmethod
    def remaining_attempts(otp: OTPModel) -> int:
        """Return remaining attempts for OTP."""
        return max(0, OTPSelector.MAX_OTP_ATTEMPTS - otp.attempts)

    @staticmethod
    def is_valid(otp: OTPModel, code: str) -> bool:
        """
        Check if OTP is valid by checking
        1. comparing code with code_hash
        2. checking if OTP is not used
        3. checking if OTP is not expired
        4. checking if remaining attempts is greater than 0
        """
        # Check if code is correct
        hashed_code = OTPSelector.hash_code(code, otp.salt)
        is_code_correct = hmac.compare_digest(hashed_code, otp.code_hash)

        if not is_code_correct:
            return False

        # Check if OTP is not used, expired, or has remaining attempts
        is_used = OTPSelector.is_used(otp)
        is_expired = OTPSelector.is_expired(otp)
        remaining_attempts = OTPSelector.remaining_attempts(otp)
        # Return True if all conditions are met
        result = not is_used and not is_expired and remaining_attempts > 0
        return result

    @staticmethod
    def hash_code(code: str, salt: str) -> str:
        """
        Return HMAC-SHA256 hex digest of code using salt.
        """
        return hmac.new(salt.encode(), code.encode(), hashlib.sha256).hexdigest()
