import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.generics import RetrieveUpdateAPIView

from accounts.api.serializers import UserSerializer

logger = logging.getLogger()


class UserAPIView(RetrieveUpdateAPIView):
    """
    API endpoint for user data.
    """

    http_method_names = ["get"]

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request: Request, *args, **kwargs):
        try:
            user = request.user
            serializer = self.serializer_class(user, context={"request": request})

            logger.info(f"User {user} requested their data via UserAPIView")
            return Response(
                {
                    "success": True,
                    "message": "User data retrieved successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error retrieving user data: {e}")
            return Response(
                {
                    "success": False,
                    "message": "Error retrieving user data.",
                    "errors": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
