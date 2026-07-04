import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse
from shop.services import CheckoutService
from shop.api.serializers import OrderSerializer

logger = logging.getLogger("shop.checkout")


class CheckoutCreateAPIView(CreateAPIView):
    """
    Checkout API view.
    """

    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            user = request.user

            order = CheckoutService.checkout(user)
            serializer = self.get_serializer(order)

            logger.info(f"Order created: {order.id}, user: {user.email}")
            return APIResponse.success(
                data=serializer.data,
                message="ثبت سفارش با موفقیت انجام شد.",
                status_code=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            msg = e.get_full_details()[0].get("message")  # type: ignore
            logger.error(f"Error while creating order: {e}")
            return APIResponse.error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f"خطا در ثبت سفارش: {msg}",
            )

        except Exception as e:
            logger.error(f"Error while creating order: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در ثبت سفارش.",
            )
