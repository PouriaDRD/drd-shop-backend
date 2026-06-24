import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import ScopedRateThrottle

from authentication.services import AuthService
from authentication.api.serializers import VerifyOTPSerializer

logger = logging.getLogger()


class OTPVerifyAPIView(APIView):
    """
    API endpoint for verifying OTP and getting JWT.
    """

    http_method_names = ["post"]

    serializer_class = VerifyOTPSerializer
    permission_classes = [AllowAny]

    throttle_scope = "verify-otp"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data

            otp_id = data["otp_id"]  # type: ignore
            code = data["code"]  # type: ignore
            phone_number = data["phone_number"]  # type: ignore

            result = AuthService.verify_otp(
                otp_id=otp_id, code=code, phone_number=phone_number
            )

            logger.info(f"OTP verified for phone_number")
            return Response(
                {
                    "success": True,
                    "message": "OTP verified.",
                    "data": result,
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            logger.error(f"Invalid OTP verification: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Error validating OTP verification.",
                    "errors": e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"Error verifying OTP: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Error verifying OTP.",
                    "errors": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
