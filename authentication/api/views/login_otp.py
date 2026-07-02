import logging

from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.exceptions import ValidationError
from config.utils import APIResponse
from authentication.api.serializers import (
    SendLoginOTPSerializer,
    VerifyLoginOTPSerializer,
)

logger = logging.getLogger("authentication.otp_login")


class SendLoginOTPAPIView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = SendLoginOTPSerializer

    throttle_scope = "otp-send"
    throttle_classes = [ScopedRateThrottle]

    http_method_names = ["post"]

    def post(self, request: Request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            result = serializer.save()

            logger.info(f"OTP sent successfully: {result['email']}")

            return APIResponse.success(
                data=result,
                message="کد ورود ارسال شد",
                status_code=status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.warning(f"Error sending OTP: {e.get_codes()}")
            return APIResponse.error(
                message=f"خطا در ارسال کد ایمیل",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"Error sending OTP: {e}")
            return APIResponse.error(
                message=f"خطا در ارسال کد ایمیل",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class VerifyLoginOTPAPIView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = VerifyLoginOTPSerializer

    throttle_scope = "otp-verify"
    throttle_classes = [ScopedRateThrottle]

    http_method_names = ["post"]

    def post(self, request: Request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            result = serializer.save()

            logger.info(f"OTP verified successfully: {result['user']}")

            return APIResponse.success(
                data=result,
                message="ورود با کد تایید انجام شد",
                status_code=status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.warning(f"Error verifying OTP: {e.get_codes()}")
            return APIResponse.error(
                message=f"کد وارد شده اشتباه یا منقضی شده است",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"Error verifying OTP: {e}")
            return APIResponse.error(
                message=f"خطا در تایید کد ایمیل",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
