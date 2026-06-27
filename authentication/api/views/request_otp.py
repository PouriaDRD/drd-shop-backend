import logging

from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from authentication.services import AuthService
from authentication.api.serializers import RequestOTPSerializer

logger = logging.getLogger("authentication")


class OTPRequestAPIView(GenericAPIView):
    """
    Request OTP.
    """

    http_method_names = ["post"]

    serializer_class = RequestOTPSerializer

    permission_classes = [AllowAny]

    throttle_scope = "request-otp"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        phone_number: str = serializer.validated_data["phone_number"]

        result = AuthService.request_otp(phone_number)

        logger.info(
            "OTP requested phone=%s",
            f"{phone_number[:4]}*****{phone_number[-2:]}",
        )

        return APIResponse.success(
            data=result,
            message="کد یکبار مصرف با موفقیت ارسال شد.",
        )
