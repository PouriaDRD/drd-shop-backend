from django.contrib.auth import authenticate

from .otp import OTPService
from .token import TokenService

from authentication.enums import OTPType
from accounts.services import UserService
from accounts.repositories import UserRepository

from authentication.exceptions import (
    WrongEmailOrPasswordError,
    UserNotFoundError,
    InvalidOTPError,
)


class AuthService:

    @classmethod
    def register(cls, email: str, password: str):

        user = UserService.create_user(
            email=email,
            password=password,
        )

        return {
            "user": str(user),
            **TokenService.generate(user),
        }

    @classmethod
    def login(cls, email: str, password: str):

        email = email.strip().lower()

        user = authenticate(username=email, password=password)

        if not user:
            raise WrongEmailOrPasswordError()

        return {
            "user": str(user),
            **TokenService.generate(user),
        }

    @classmethod
    def send_login_otp(cls, email: str, otp_type: OTPType = OTPType.LOGIN):

        email = email.strip().lower()

        otp = OTPService.send_otp(email, otp_type)

        return {
            "email": email,
            "message": "OTP sent successfully",
            "expires_in": OTPService.OTP_TTL_MINUTES,
        }

    @classmethod
    def verify_login_otp(cls, email: str, code: str, otp_type: OTPType = OTPType.LOGIN):

        email = email.strip().lower()

        is_valid = OTPService.verify_otp(email, code, otp_type)

        if not is_valid:
            raise InvalidOTPError()

        user = UserRepository.get_by_email(email)

        if not user or not user.is_active:
            raise UserNotFoundError()

        if not user.email_verified:
            user.email_verified = True
            UserRepository.save(user, update_fields=["email_verified"])

        return {
            "user": str(user),
            **TokenService.generate(user),
        }
