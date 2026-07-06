import secrets
from django.db import transaction

from authentication.enums import OTPType
from config.settings.app_config import config
from authentication.selectors import OTPSelector
from authentication.repositories import OTPRepository

# from django.core.mail import send_mail
from notifications.tasks import send_email_task


class OTPService:
    """
    Service layer responsible for generating, sending, validating,
    and enforcing rules for OTP codes.
    """

    OTP_LENGTH = config.auth.otp_length
    OTP_TTL_MINUTES = config.auth.otp_ttl_minutes
    MAX_OTP_ATTEMPTS = config.auth.max_otp_attempts

    @classmethod
    @transaction.atomic
    def send_otp(cls, email: str, otp_type: OTPType):
        """
        Generates a new OTP, enforces existing cooldown limits,
        """

        # 1. Remove expired OTPs to keep DB clean
        OTPRepository.delete_expired_otp(email)

        # 2. Check if a usable OTP already exists
        pending_otp = OTPRepository.get_active_otp(email, otp_type)
        is_expired = OTPSelector.is_expired(pending_otp)
        if pending_otp and not is_expired:
            return

        # 3. Generate new OTP
        otp_code = cls._generate_otp_code()
        otp_salt = secrets.token_hex(16)
        otp_hash = OTPSelector.hash_code(otp_code, otp_salt)

        # 4. Save OTP in repository
        otp_instance = OTPRepository.create_otp(
            email=email,
            otp_type=otp_type,
            salt=otp_salt,
            code_hash=otp_hash,
        )

        # 5. Send OTP to user
        # send_mail(
        #     "test",
        #     "hello",
        #     "31j.mac.t3@gmail.com",
        #     ["pouriadrd@gmail.com"],
        #     fail_silently=False,
        # )
        cls.send_otp_to_email(email, otp_code)
        # TODO: Send it with email service
        # cls._print_to_terminal(email, otp_code)

        return otp_instance

    @classmethod
    @transaction.atomic
    def verify_otp(cls, email: str, code: str, otp_type: OTPType) -> bool:
        """
        Validates an OTP against the stored hashed code, enforcing
        expiration rules and incrementing attempt counters.
        """

        # 1. Retrieve the pending OTP
        pending_otp = OTPRepository.get_active_otp(email, otp_type)
        if not pending_otp:
            return False

        # 2. Increase attempt count (stored in DB)
        OTPRepository.increment_attempts(pending_otp)

        # 3. Check validity
        is_valid = OTPSelector.is_valid(pending_otp, code)

        if is_valid:
            OTPRepository.mark_used(pending_otp)
            return True

        return False

    @classmethod
    def _print_to_terminal(cls, email: str, code: str):
        print(f"[OTP] {email} => {code}")

    @classmethod
    def send_otp_to_email(cls, email: str, code: str):
        """
        Sends an OTP to the user via email.
        """

        send_email_task.delay(
            template_slug="otp-template",
            recipient_email=email,
            recipient_name=email,
            context={
                "name": email,
                "otp_code": code,
                "expiry_minutes": cls.OTP_TTL_MINUTES,
                "site_name": "DRD Shop",
                "support_email": "31j.mac.t3@gmail.com",
            },
        )  # type: ignore

    @classmethod
    def _generate_otp_code(cls) -> str:
        code = f"{secrets.randbelow(10 ** cls.OTP_LENGTH):0{cls.OTP_LENGTH}d}"
        return code
