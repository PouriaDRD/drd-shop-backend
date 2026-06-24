import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import ScopedRateThrottle

from authentication.services import AuthService
from authentication.api.serializers import RequestOTPSerializer

logger = logging.getLogger()


class OTPRequestAPIView(APIView):
    """
    API endpoint for requesting OTP.
    """

    http_method_names = ["post"]

    permission_classes = [AllowAny]
    serializer_class = RequestOTPSerializer

    throttle_scope = "request-otp"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            phone_number = serializer.validated_data["phone_number"]  # type: ignore

            result = AuthService.request_otp(phone_number)
            logger.info(f"OTP sent to {phone_number}")
            return Response(
                {
                    "success": True,
                    "message": f"OTP sent to {phone_number}.",
                    "data": result,
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            logger.error(f"Invalid OTP request: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Error validating OTP request.",
                    "errors": e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"Error requesting OTP: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Error requesting OTP.",
                    "errors": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
