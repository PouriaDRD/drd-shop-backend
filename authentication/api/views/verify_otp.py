import logging

from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse

from authentication.services import AuthService
from authentication.api.serializers import VerifyOTPSerializer

logger = logging.getLogger("authentication")


class OTPVerifyAPIView(GenericAPIView):
    """
    Verify OTP and issue JWT tokens.
    """

    http_method_names = ["post"]

    serializer_class = VerifyOTPSerializer

    permission_classes = [AllowAny]

    throttle_scope = "verify-otp"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        result = AuthService.verify_otp(
            otp_id=data["otp_id"],
            code=data["code"],
            phone_number=data["phone_number"],
        )

        logger.info(
            "OTP verified for %s",
            f"{data['phone_number'][:4]}*****{data['phone_number'][-2:]}",
        )

        return APIResponse.success(
            data=result,
            message="OTP verified successfully.",
        )
