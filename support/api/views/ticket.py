import logging
from rest_framework.request import Request
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from config.utils import APIResponse


from support.services import TicketService

from support.api.serializers import (
    TicketCreateSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
    TicketReplySerializer,
)

logger = logging.getLogger("support.ticket")


class TicketCreateAPIView(CreateAPIView):
    """
    Create new ticket.
    """

    http_method_names = ["post"]

    permission_classes = [IsAuthenticated]

    serializer_class = TicketCreateSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def create(self, request: Request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            ticket = serializer.save()

            logger.info(
                f"Ticket created successfully: {str(ticket.id)}, user={str(ticket.user)}"
            )
            return APIResponse.success(
                data={
                    "id": str(ticket.id),
                },
                message="تیکت با موفقیت ایجاد شد.",
                status_code=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            logger.error(f"Error creating ticket: {e}")
            return APIResponse.error(
                message=f"خطا در ایجاد تیکت رخ داد: داده ها معتبر نمی باشند",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            return APIResponse.error(
                message="خطا در ایجاد تیکت رخ داد.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TicketListAPIView(ListAPIView):
    """
    User tickets.
    """

    http_method_names = ["get"]

    permission_classes = [IsAuthenticated]

    serializer_class = TicketListSerializer

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_queryset(self):  # type: ignore

        return TicketService.get_user_tickets(self.request.user)

    def get(self, request: Request, *args, **kwargs):
        try:
            user = request.user
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            logger.info(f"User tickets retrieved: {str(user)}")
            return APIResponse.success(
                data=serializer.data,
                message="تیکت های کاربر با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error getting user tickets: {e}")
            return APIResponse.error(
                message="خطا در دریافت تیکت های کاربر رخ داد.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TicketDetailAPIView(RetrieveAPIView):
    """
    Ticket detail.
    """

    http_method_names = ["get"]

    permission_classes = [IsAuthenticated]

    serializer_class = TicketDetailSerializer

    lookup_field = "id"

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get_object(self):  # type: ignore

        return TicketService.get_ticket(
            ticket_id=self.kwargs["id"],
            user=self.request.user,
        )

    def get(self, request: Request, *args, **kwargs):
        try:
            ticket = self.get_object()
            serializer = self.get_serializer(ticket)

            logger.info(f"Ticket detail retrieved: {str(ticket.id)}")
            return APIResponse.success(
                data=serializer.data,
                message="تیکت با موفقیت دریافت شد.",
                status_code=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error getting ticket detail: {e}")
            return APIResponse.error(
                message="خطا در دریافت تیکت رخ داد.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TicketReplyAPIView(APIView):
    """
    Reply to ticket.
    """

    http_method_names = ["post"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            id = kwargs["id"]

            serializer = TicketReplySerializer(
                data=request.data,
                context={
                    "request": request,
                    "ticket_id": id,
                },
            )

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return APIResponse.success(
                message="پاسخ شما ثبت شد.",
            )

        except ValidationError as e:
            logger.error(f"Error replying to ticket: {e}")
            return APIResponse.error(
                message="خطا در پاسخ تیکت رخ داد.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.error(f"Error replying to ticket: {e}")
            return APIResponse.error(
                message="خطا در پاسخ تیکت رخ داد.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TicketCloseAPIView(APIView):
    """
    Close ticket.
    """

    http_method_names = ["post"]

    permission_classes = [IsAuthenticated]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):

        try:
            id = kwargs["id"]

            ticket = TicketService.close(
                ticket_id=id,
                user=request.user,
            )

            return APIResponse.success(
                data={
                    "status": ticket.status,
                },
                message="تیکت بسته شد.",
            )
        except Exception as e:
            logger.error(f"Error closing ticket: {e}")
            return APIResponse.error(
                message="خطا در بستن تیکت رخ داد.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
