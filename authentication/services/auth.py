import logging
import secrets
from datetime import timedelta

from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from config.settings.app_config import config

from accounts.services import UserService
from accounts.selectors import UserSelector
from accounts.repositories import UserRepository

from authentication.models import OTPModel
from authentication.selectors import OTPSelector
from authentication.repositories import OTPRepository

logger = logging.getLogger()


class AuthService:
    """
    Authentication flow:
    OTP generation → validation → JWT issuance
    """

    OTP_LENGTH = config.auth.otp_length
    OTP_TTL_MINUTES = config.auth.otp_ttl_minutes
    MAX_OTP_ATTEMPTS = config.auth.max_otp_attempts

    @classmethod
    def _generate_otp_code(cls) -> str:
        return f"{secrets.randbelow(10 ** cls.OTP_LENGTH):06d}"

    @classmethod
    def request_otp(cls, phone_number: str):
        code = cls._generate_otp_code()
        expires_at = timezone.now() + timedelta(minutes=cls.OTP_TTL_MINUTES)

        otp = OTPRepository.create_otp_code(
            phone_number=phone_number,
            code=code,
            expires_at=expires_at,
        )

        cls._send_otp(phone_number, code)

        return {
            "otp_id": otp.id,
            "phone_number": phone_number,
        }

    @classmethod
    def verify_otp(cls, otp_id: str, code: str, phone_number: str):
        otp = OTPRepository.get_otp_by_id(otp_id)

        if not otp:
            raise ValidationError("Invalid OTP.")

        cls._validate_otp(otp, code, phone_number)

        OTPRepository.mark_as_verified(otp)

        user = UserRepository.get_by_phone(otp.phone_number)

        if not user:
            user = UserService.create_user(phone_number)

            UserRepository.update_last_login(user)
            refresh = RefreshToken.for_user(user)

            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "is_active": True,
                "registered": True,
            }

        else:
            is_active = UserSelector.is_active(user)
            if not is_active:
                raise ValidationError("User not found or inactive.")
            else:
                UserRepository.update_last_login(user)
                refresh = RefreshToken.for_user(user)

                return {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "is_active": True,
                    "registered": False,
                }

    @classmethod
    def _validate_otp(cls, otp: OTPModel, code, phone_number):
        if otp.attempts >= cls.MAX_OTP_ATTEMPTS:
            raise ValidationError("Too many attempts.")

        if otp.is_verified:
            OTPRepository.increment_attempts(otp)
            raise ValidationError("OTP already used.")

        if OTPSelector.is_expired(otp):
            OTPRepository.increment_attempts(otp)
            raise ValidationError("OTP expired.")

        if otp.phone_number != phone_number:
            OTPRepository.increment_attempts(otp)
            raise ValidationError("Phone mismatch.")

        if otp.code != code.strip():
            OTPRepository.increment_attempts(otp)
            raise ValidationError("Wrong OTP.")

    @staticmethod
    def _send_otp(phone_number: str, code: str):
        print("============ OTP Code =============")
        print(f"Phone: {phone_number}")
        print(f"Code:  {code}")
        print("====================================\n")
