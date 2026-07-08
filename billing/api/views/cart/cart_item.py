import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.generics import DestroyAPIView, UpdateAPIView, CreateAPIView
from billing.services.cart import CartService
from billing.repositories.cart import CartItemRepository
from billing.api.serializers import (
    CartSerializer,
    AddCartItemSerializer,
    CartItemSerializer,
    UpdateCartItemSerializer,
)

from config.utils import APIResponse
from commerce.models import ProductModel, ProductPlanModel

logger = logging.getLogger("billing.cart-item")


class AddCartItemAPIView(CreateAPIView):
    """
    Add a cart item.
    """

    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    serializer_class = AddCartItemSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product = ProductModel.objects.get(
                id=serializer.validated_data["product_id"]
            )
            plan = ProductPlanModel.objects.get(id=serializer.validated_data["plan_id"])

            cart, item = CartService.add_item(
                request.user,
                product=product,
                plan=plan,
                quantity=serializer.validated_data["quantity"],
                is_renewal=serializer.validated_data["is_renewal"],
                service_id=serializer.validated_data["service_id"],
            )

            logger.info(
                f"Cart item added: user: {request.user}, cart: {cart.id}, product: {product.title}, plan: {plan.title}"
            )

            item_data = CartItemSerializer(item).data

            return APIResponse.success(
                data={
                    "cart": CartSerializer(cart).data,
                    "item": item_data,
                },
                status_code=status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.error(f"Error while adding cart item: {e}")
            return APIResponse.error(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=f"{e.get_full_details()[0].get('message')}",  # type: ignore
            )

        except Exception as e:
            logger.error(f"Error while adding cart item: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در افزودن محصول.",
            )


class UpdateCartItemAPIView(UpdateAPIView):
    """
    Update a cart item.
    """

    http_method_names = ["patch"]
    permission_classes = [IsAuthenticated]

    serializer_class = UpdateCartItemSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def patch(self, request: Request, *args, **kwargs):
        try:
            item_id = kwargs["item_id"]
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            item = CartItemRepository.get(item_id)
            quantity = int(serializer.validated_data["quantity"])
            CartService.update_item(item, quantity=quantity)

            logger.info(f"Cart item updated: {item.id}")
            return APIResponse.success(
                data={
                    "cart": CartSerializer(item.cart).data,
                    "item": CartItemSerializer(item).data,
                },
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error while updating cart item: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در بروزرسانی محصول.",
            )


class DeleteCartItemAPIView(DestroyAPIView):
    """
    Delete a cart item.
    """

    http_method_names = ["delete"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def delete(self, request: Request, *args, **kwargs):
        try:
            item_id = kwargs["item_id"]
            item = CartItemRepository.get(item_id)
            CartService.remove_item(item)

            logger.info(f"Cart item deleted: {item.id}")
            return APIResponse.success(
                data={
                    "id": str(item.id),
                    "deleted": True,
                },
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error while deleting cart item: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در حذف محصول.",
            )
