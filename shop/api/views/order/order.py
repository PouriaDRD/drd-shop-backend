import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from shop.repositories.order import OrderRepository
from shop.api.serializers.order import OrderSerializer

logger = logging.getLogger("shop.order_view")


class OrderListAPIView(ListAPIView):
    """
    List all orders.
    """

    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore
        user = self.request.user
        return OrderRepository.get_user_orders(user)  # type: ignore

    def get(self, request: Request, *args, **kwargs):
        try:
            orders = self.get_queryset()
            serializer = self.get_serializer(orders, many=True)

            logger.info(f"Orders retrieved for user: {str(request.user)}")

            return APIResponse.success(
                data=serializer.data,
                message="سفارشات با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error while retrieving orders: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در دریافت سفارشات.",
            )
