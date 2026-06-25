import logging
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from accounts.api.serializers import UserSerializer

logger = logging.getLogger("accounts")


class UserAPIView(RetrieveAPIView):
    """
    Retrieve authenticated user.
    """

    http_method_names = ["get"]

    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request: Request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        logger.info("User data retrieved")

        return APIResponse.success(
            data=serializer.data,
            message="User data retrieved successfully.",
        )
