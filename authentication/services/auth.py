import secrets
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


from accounts.services import UserService
from accounts.selectors import UserSelector
from config.settings.app_config import config
from accounts.repositories import UserRepository
from authentication.repositories import OTPRepository


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
        code = f"{secrets.randbelow(10 ** cls.OTP_LENGTH):0{cls.OTP_LENGTH}d}"
        return code

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
    @transaction.atomic
    def verify_otp(cls, otp_id: str, code: str, phone_number: str):

        # 1. SINGLE QUERY
        otp = OTPRepository.select_for_update(otp_id)

        if not otp:
            raise ValidationError("کد یکبار مصرف معتبر نیست.")

        # 2. fast validations (no DB calls)
        if otp.is_verified:
            raise ValidationError("کد یکبار مصرف قبلا تایید شده است.")

        if otp.expires_at < timezone.now():
            raise ValidationError("کد یکبار مصرف منقضی شده است.")

        if otp.attempts >= cls.MAX_OTP_ATTEMPTS:
            raise ValidationError("کد یکبار مصرف منقضی شده است.")

        if otp.phone_number != phone_number:
            OTPRepository.increment_attempts(otp)
            raise ValidationError("شماره تلفن مورد نظر مطابقت ندارد.")

        if otp.code != code.strip():
            OTPRepository.increment_attempts(otp)
            raise ValidationError("کد نادرست می باشد.")

        # 3. mark verified ONCE
        OTPRepository.mark_verified(otp)

        # 4. get or create user (SINGLE PATH)
        user = UserRepository.get_by_phone(phone_number)
        is_new = False

        if not user:
            is_new = True
            user = UserService.create_user(phone_number)

        if not UserSelector.is_active(user):
            raise ValidationError("User inactive.")

        UserRepository.update_last_login(user)

        # 5. tokens
        tokens = cls._create_tokens(user)

        return {
            "tokens": tokens,
            "is_new": is_new,
        }

    @classmethod
    def _create_tokens(cls, user):
        refresh = RefreshToken.for_user(user)

        access_token = refresh.access_token

        # Expiry calculation
        access_expires = timezone.now() + api_settings.ACCESS_TOKEN_LIFETIME  # type: ignore
        refresh_expires = timezone.now() + api_settings.REFRESH_TOKEN_LIFETIME  # type: ignore

        return {
            "access": str(access_token),
            "refresh": str(refresh),
            "access_expires_at": access_expires.isoformat(),
            "refresh_expires_at": refresh_expires.isoformat(),
        }

    @staticmethod
    def _send_otp(phone_number: str, code: str):
        print("============ OTP Code =============")
        print(f"Phone: {phone_number}")
        print(f"Code:  {code}")
        print("====================================\n")
