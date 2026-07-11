from user_agents import parse

from rest_framework.request import Request
from django.contrib.auth import authenticate

from .otp import OTPService
from .token import TokenService
from .login_history import LoginHistoryService

from accounts.models import UserModel

from notifications.tasks import send_email_task
from notifications.services import NotificationService

from authentication.enums import OTPType
from authentication.exceptions import (
    WrongEmailOrPasswordError,
    UserNotFoundError,
    InvalidOTPError,
)

from accounts.repositories import UserRepository
from accounts.services import UserService, ReferralService


class AuthService:
    """
    Authentication business logic.
    """

    SITE_NAME = "DRD Shop"

    @classmethod
    def register(
        cls,
        email: str,
        password: str,
        referral_code: str,
        request: Request,
    ):
        email = cls.normalize_email(email)

        user = UserService.create_user(
            email=email,
            password=password,
        )

        ReferralService.create_referral_code(user)

        if referral_code:
            ReferralService.apply_referral_code(
                user=user,
                code=referral_code,
            )

        cls.send_auth_email(
            template="register-success",
            request=request,
            user=user,
        )

        NotificationService.create_success(
            user=user,
            title="ثبت نام موفق بود!",
            message="حساب شما با موفقیت ثبت نام شد.",
        )

        LoginHistoryService.create_success(
            user,
            request,
        )

        cls.alert_admin(user)

        return cls.auth_response(user)

    @classmethod
    def login(
        cls,
        email: str,
        password: str,
        request: Request,
    ):
        email = cls.normalize_email(email)

        user = authenticate(
            request=request,  # type: ignore
            username=email,
            password=password,
        )

        if not user:
            cls.handle_failed_login(
                email=email,
                request=request,
                reason="نام کاربری یا رمز عبور اشتباه است.",
            )

            raise WrongEmailOrPasswordError()

        if user.email_verified:  # type: ignore
            cls.send_auth_email(
                template="login-success",
                request=request,
                user=user,
            )

        return cls.auth_response(user)

    @classmethod
    def send_login_otp(
        cls,
        email: str,
        otp_type: OTPType = OTPType.LOGIN,
    ):

        email = cls.normalize_email(email)

        OTPService.send_otp(
            email,
            otp_type,
        )

        return {
            "email": email,
            "message": "OTP sent successfully",
            "expires_in": OTPService.OTP_TTL_MINUTES,
        }

    @classmethod
    def verify_login_otp(
        cls,
        email: str,
        code: str,
        request: Request,
        otp_type: OTPType = OTPType.LOGIN,
    ):

        email = cls.normalize_email(email)

        if not OTPService.verify_otp(
            email,
            code,
            otp_type,
        ):

            cls.handle_failed_login(
                email=email,
                request=request,
                reason="کد یکبار مصرف نامعتبر است.",
            )

            raise InvalidOTPError()

        user = UserRepository.get_by_email(email)

        if not user or not user.is_active:
            raise UserNotFoundError()

        if not user.email_verified:
            user.email_verified = True

            UserRepository.save(
                user,
                update_fields=["email_verified"],
            )

        cls.send_auth_email(
            template="login-success",
            request=request,
            user=user,
        )

        NotificationService.create_success(
            user=user,
            title="ورود موفق بود!",
            message="شما با موفقیت وارد حساب خود شدید.",
        )

        LoginHistoryService.create_success(
            user,
            request,
        )

        return cls.auth_response(user)

    @classmethod
    def handle_failed_login(
        cls,
        email: str,
        request: Request,
        reason: str,
    ):

        LoginHistoryService.create_failed(
            email,
            request,
            reason,
        )

        info = LoginHistoryService.get_login_info(request)

        NotificationService.create_warning(
            email=email,
            title="ورود ناموفق بود!",
            message=(
                "یک تلاش ناموفق به حساب شما صورت گرفت.\n"
                f"IP: {info['ip_address']}\n"
                f"Device: {info['device']}\n"
                f"Browser: {info['browser']}\n"
                f"OS: {info['os']}"
            ),
        )

    @classmethod
    def send_auth_email(
        cls,
        template: str,
        request: Request,
        user,
    ):

        info = cls.get_device_info(request)

        send_email_task.delay(
            template_slug=template,
            recipient_email=user.email,
            recipient_name=str(user),
            context={
                "name": str(user),
                "device": info["device"],
                "browser": info["browser"],
                "ip_address": cls.get_client_ip(request),
                "site_name": cls.SITE_NAME,
            },
        )  # type: ignore

    @classmethod
    def alert_admin(cls, user: UserModel):
        """
        Send admin notification for user approval.
        """

        admin_user = UserRepository.get_admin_user()

        if not admin_user:
            return

        NotificationService.create_success(
            user=admin_user,
            title="کاربر ثبت شد!",
            message=(f"کاربر «{user.email}» ثبت شد.\n" f"کاربر: {str(user)}\n"),
        )

    @classmethod
    def get_device_info(
        cls,
        request: Request,
    ):

        ua = parse(
            request.META.get(
                "HTTP_USER_AGENT",
                "",
            )
        )

        return {
            "browser": (f"{ua.browser.family} " f"{ua.browser.version_string}"),
            "device": (
                "Mobile" if ua.is_mobile else "Tablet" if ua.is_tablet else "PC"
            ),
            "os": (f"{ua.os.family} " f"{ua.os.version_string}"),
        }

    @classmethod
    def get_client_ip(
        cls,
        request: Request,
    ):

        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

        if forwarded:
            return forwarded.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR")

    @classmethod
    def normalize_email(
        cls,
        email: str,
    ):
        return email.strip().lower()

    @classmethod
    def auth_response(
        cls,
        user,
    ):

        return {
            "user": str(user),
            **TokenService.generate(user),
        }
