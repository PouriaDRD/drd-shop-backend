import logging
from django.http import Http404
from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)

from config.utils import APIResponse
from support.models import TicketModel
from support.services import TicketService
from support.api.serializers import (
    TicketReplySerializer,
    AdminTicketListSerializer,
    AdminTicketDetailSerializer,
)

logger = logging.getLogger("support.admin-ticket")


class AdminTicketListAPIView(ListAPIView):
    """
    Return all tickets created by admin users.
    """

    http_method_names = ["get"]

    permission_classes = [IsAdminUser]

    serializer_class = AdminTicketListSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore
        return TicketService.get_all_tickets()

    def list(self, request: Request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            serializer = self.get_serializer(
                queryset,
                many=True,
            )

            logger.info(
                "Admin '%s' retrieved admin tickets.",
                request.user,
            )

            return APIResponse.success(
                data=serializer.data,
                message="تیکت‌های ادمین با موفقیت دریافت شدند.",
                status_code=status.HTTP_200_OK,
            )

        except Exception:
            logger.exception("Failed to retrieve admin tickets.")

            return APIResponse.error(
                message="خطا در دریافت تیکت‌های ادمین رخ داد.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminTicketDetailAPIView(RetrieveAPIView):
    """
    Retrieve any ticket for administrators.
    """

    http_method_names = ["get"]

    permission_classes = [IsAdminUser]

    serializer_class = AdminTicketDetailSerializer

    lookup_field = "id"

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_object(self):  # type: ignore
        return TicketService.get_admin_ticket(
            ticket_id=self.kwargs["id"],
        )

    def retrieve(self, request: Request, *args, **kwargs):
        try:
            ticket = self.get_object()

            serializer = self.get_serializer(
                ticket,
                context={"request": request},
            )

            logger.info(
                "Admin '%s' retrieved ticket '%s'.",
                request.user,
                ticket.id,
            )

            return APIResponse.success(
                data=serializer.data,
                message="تیکت با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )

        except TicketModel.DoesNotExist:
            return APIResponse.error(
                message="تیکت مورد نظر یافت نشد.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        except Http404:
            return APIResponse.error(
                message="تیکت مورد نظر یافت نشد.",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        except Exception:
            logger.exception("Failed to retrieve admin ticket.")

            return APIResponse.error(
                message="خطا در دریافت تیکت رخ داد.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AdminTicketReplyAPIView(APIView):
    """
    Reply to a ticket as an administrator.
    """

    http_method_names = ["post"]

    permission_classes = [IsAdminUser]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def post(self, request: Request, *args, **kwargs):
        try:
            serializer = TicketReplySerializer(
                data=request.data,
            )

            serializer.is_valid(raise_exception=True)

            TicketService.admin_reply(
                ticket_id=kwargs["id"],
                admin=request.user,
                message=serializer.validated_data["message"],  # type: ignore
                attachments=serializer.validated_data.get("attachments"),  # type: ignore
            )

            logger.info(
                "Admin '%s' replied to ticket '%s'.",
                request.user,
                kwargs["id"],
            )

            return APIResponse.success(
                message="پاسخ با موفقیت ارسال شد.",
            )

        except ValidationError:
            return APIResponse.error(
                message="اطلاعات ارسالی معتبر نیست.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except ValueError as exc:
            return APIResponse.error(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:
            logger.exception(
                "Failed to reply to ticket '%s'.",
                kwargs["id"],
            )

            return APIResponse.error(
                message="خطا در ثبت پاسخ تیکت رخ داد.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
