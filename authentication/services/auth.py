from user_agents import parse
from rest_framework.request import Request
from django.contrib.auth import authenticate

from .otp import OTPService
from .token import TokenService

from notifications.tasks import send_email_task
from notifications.enums import NotificationType
from notifications.services import NotificationService

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
    def register(cls, email: str, password: str, request: Request):
        user = UserService.create_user(
            email=email,
            password=password,
        )

        cls.send_register_notification_email(
            request,
            str(user),
            email,
        )

        NotificationService.create(
            user=user,
            title="ثبت نام موفق بود!",
            message="حساب شما با موفقیت ثبت نام شد. از اینکه مارو انتخاب کردین ممنونیم!",
            notification_type=NotificationType.INFO,
        )

        return {
            "user": str(user),
            **TokenService.generate(user),
        }

    @classmethod
    def login(cls, email: str, password: str, request: Request):

        email = email.strip().lower()

        user = authenticate(username=email, password=password)

        if not user:
            raise WrongEmailOrPasswordError()

        if user.email_verified:  # type: ignore
            cls.send_login_notification_email(
                request,
                name=str(user),
                email=user.email,
            )

        NotificationService.create(
            user=user,  # type: ignore
            title="ورود موفق بود!",
            message="شما با موفقیت وارد حساب خود شدید!",
            notification_type=NotificationType.INFO,
        )

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
    def verify_login_otp(
        cls,
        email: str,
        code: str,
        request: Request,
        otp_type: OTPType = OTPType.LOGIN,
    ):

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

        cls.send_login_notification_email(
            request,
            name=str(user),
            email=user.email,
        )

        NotificationService.create(
            user=user,  # type: ignore
            title="ورود موفق بود!",
            message="شما با موفقیت وارد حساب خود شدید!",
            notification_type=NotificationType.INFO,
        )

        return {
            "user": str(user),
            **TokenService.generate(user),
        }

    @classmethod
    def send_register_notification_email(cls, request: Request, name: str, email: str):

        name = str(name)
        email = str(email)

        user_agent_string = request.META.get("HTTP_USER_AGENT", "")
        ua = parse(user_agent_string)

        browser = f"{ua.browser.family} {ua.browser.version_string}"
        device = "Mobile" if ua.is_mobile else "PC" if ua.is_pc else "Tablet"

        send_email_task.delay(
            template_slug="register-success",
            recipient_email=email,
            recipient_name=name,
            context={
                "name": name,
                "device": device,
                "browser": browser,
                "ip_address": cls.get_client_ip(request),
                # "login_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                # "location": "Unknown",
                "site_name": "DRD Shop",
            },
        )  # type: ignore

    @classmethod
    def send_login_notification_email(cls, request: Request, name: str, email: str):

        name = str(name)
        email = str(email)

        user_agent_string = request.META.get("HTTP_USER_AGENT", "")
        ua = parse(user_agent_string)

        browser = f"{ua.browser.family} {ua.browser.version_string}"
        device = "Mobile" if ua.is_mobile else "PC" if ua.is_pc else "Tablet"

        send_email_task.delay(
            template_slug="login-success",
            recipient_email=email,
            recipient_name=name,
            context={
                "name": name,
                "device": device,
                "browser": browser,
                "ip_address": cls.get_client_ip(request),
                # "login_time": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                # "location": "Unknown",
                "site_name": "DRD Shop",
            },
        )  # type: ignore

    @classmethod
    def get_client_ip(cls, request: Request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
