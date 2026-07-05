import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from commerce.api.serializers import V2rayVPNSerializer
from commerce.repositories import V2rayVPNRepository

logger = logging.getLogger("commerce.v2ray-vpn-service")


class V2rayVPNListAPIView(ListAPIView):
    """
    List all VPN services.
    """

    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    serializer_class = V2rayVPNSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return V2rayVPNRepository.get_user_vpn_services(user)  # type: ignore

    def get(self, request: Request, *args, **kwargs):
        try:
            vpns = self.get_queryset()
            serializer = self.get_serializer(vpns, many=True)

            logger.info(f"VPN services retrieved for user: {str(request.user)}")

            return APIResponse.success(
                data=serializer.data,
                message="VPN services retrieved.",
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error while retrieving VPN services: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در دریافت VPN سرویس.",
            )
