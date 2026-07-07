from django.urls import path

from support.api.views import (
    TicketCreateAPIView,
    TicketListAPIView,
    TicketDetailAPIView,
    TicketReplyAPIView,
    TicketCloseAPIView,
)

urlpatterns = [
    path(
        "my-tickets/",
        TicketListAPIView.as_view(),
        name="ticket-list",
    ),
    path(
        "my-tickets/create/",
        TicketCreateAPIView.as_view(),
        name="ticket-create",
    ),
    path(
        "my-tickets/<uuid:id>/",
        TicketDetailAPIView.as_view(),
        name="ticket-detail",
    ),
    path(
        "my-tickets/<uuid:id>/reply/",
        TicketReplyAPIView.as_view(),
        name="ticket-reply",
    ),
    path(
        "my-tickets/<uuid:id>/close/",
        TicketCloseAPIView.as_view(),
        name="ticket-close",
    ),
]
