import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from authentication.api.serializers import LoginSerializer

logger = logging.getLogger("authentication.login")


class LoginAPIView(GenericAPIView):
    """
    User login endpoint.
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    throttle_scope = "login"
    throttle_classes = [ScopedRateThrottle]

    http_method_names = ["post"]

    def post(self, request: Request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            result = serializer.save()

            logger.info(f"User logged in successfully: {result['user']}")
            return APIResponse.success(
                data=result,
                message="ورود با موفقیت انجام شد.",
                status_code=status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.warning(f"Error registering user: {e.get_codes()}")
            return APIResponse.error(
                message=f"خطا در ورود حساب کاربری",
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=f"خطا در ورود حساب کاربری",
            )

        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            return APIResponse.error(
                message=f"خطا در ورود به سیستم",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                errors=f"خطا در ورود حساب کاربری",
            )
