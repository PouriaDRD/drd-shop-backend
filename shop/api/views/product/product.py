import logging
from rest_framework import status
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.generics import ListAPIView, RetrieveAPIView

from config.utils import APIResponse
from shop.repositories import ProductRepository
from shop.api.serializers import ProductSerializer, ProductDetailSerializer

logger = logging.getLogger("shop.product-list")


class ProductListAPIView(ListAPIView):
    """
    List all active products.
    """

    http_method_names = ["get"]

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    throttle_scope = "anon"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore
        return ProductRepository.get_all()

    def get(self, request: Request, *args, **kwargs):
        """
        Return all active products.
        """
        try:
            queryset = self.get_queryset()

            serializer = self.get_serializer(queryset, many=True)

            logger.info(f"Products retrieved: {queryset.count()} items")

            return APIResponse.success(
                data=serializer.data,
                message="محصولات با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error while retrieving products: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در دریافت محصولات.",
            )


class ProductDetailAPIView(RetrieveAPIView):
    """
    Retrieve a product by id.
    """

    http_method_names = ["get"]

    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

    throttle_scope = "anon"
    throttle_classes = [ScopedRateThrottle]

    lookup_field = "product_id"

    def get_object(self):  # type: ignore
        obj = ProductRepository.get_by_id(self.kwargs["product_id"])

        if not obj:
            raise Exception("NOT_FOUND")

        return obj

    def get(self, request: Request, *args, **kwargs):
        """
        Return a product by id.
        """

        try:
            obj = self.get_object()
            serializer = self.get_serializer(obj)

            logger.info(f"Product detail retrieved: {obj.id}")

            return APIResponse.success(
                data=serializer.data,
                message="جزئیات محصول با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            # Custom NotFound handling
            if str(e) == "NOT_FOUND":
                logger.error(f"Product not found: {self.kwargs['product_id']}")
                return APIResponse.error(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="محصول یافت نشد.",
                )

            logger.error(f"Error while retrieving product: {e}")
            return APIResponse.error(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="خطا در دریافت جزئیات محصول.",
            )
