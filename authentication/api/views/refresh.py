from datetime import timedelta
from typing import cast

from django.utils import timezone

from rest_framework import status
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.settings import api_settings

from config.utils import APIResponse

from authentication.api.serializers import (
    CustomTokenRefreshSerializer,
)


class TokenRefreshAPIView(GenericAPIView):
    """
    Refresh JWT access token.
    """

    http_method_names = ["post"]

    permission_classes = [AllowAny]

    serializer_class = CustomTokenRefreshSerializer

    throttle_scope = "refresh-token"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        access_lifetime = cast(
            timedelta,
            api_settings.ACCESS_TOKEN_LIFETIME,
        )

        access_expires_at = timezone.now() + access_lifetime

        return APIResponse.success(
            data={
                "access": serializer.validated_data["access"],
                "access_expires_at": access_expires_at.isoformat(),
            },
            message="Token refreshed successfully.",
            status_code=status.HTTP_200_OK,
        )
