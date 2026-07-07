from django.contrib import admin
from django.utils import timezone

from support.models import (
    TicketModel,
    TicketMessageModel,
    TicketAttachmentModel,
)

from support.enums import TicketStatus
from support.services import TicketService

# ==================================================
# Attachment Inline
# ==================================================


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachmentModel

    extra = 0

    readonly_fields = (
        "id",
        "created_at",
    )


# ==================================================
# Message Inline
# ==================================================


class TicketMessageInline(admin.TabularInline):
    model = TicketMessageModel

    extra = 0

    fields = (
        "sender",
        "message",
        "is_staff_reply",
    )


# ==================================================
# Ticket Admin
# ==================================================


@admin.register(TicketModel)
class TicketAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "title",
        "category",
        "status",
        "priority",
        "created_at",
    )

    search_fields = (
        "user__email",
        "title",
    )

    list_filter = (
        "status",
        "priority",
        "created_at",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    inlines = [
        TicketMessageInline,
    ]

    actions = [
        "close_tickets",
        "reopen_tickets",
    ]

    # -----------------------------------------
    # Close Tickets
    # -----------------------------------------

    @admin.action(description="Close selected tickets")
    def close_tickets(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            status=TicketStatus.CLOSED,
        )

        self.message_user(
            request,
            f"{updated} tickets closed successfully.",
        )

    # -----------------------------------------
    # Reopen Tickets
    # -----------------------------------------

    @admin.action(description="Reopen selected tickets")
    def reopen_tickets(
        self,
        request,
        queryset,
    ):

        updated = queryset.update(
            status=TicketStatus.OPEN,
        )

        self.message_user(
            request,
            f"{updated} tickets reopened successfully.",
        )


# ==================================================
# Message Admin
# ==================================================


@admin.register(TicketMessageModel)
class TicketMessageAdmin(admin.ModelAdmin):

    list_display = (
        "ticket",
        "sender",
        "short_message",
        "created_at",
    )

    search_fields = (
        "ticket__id",
        "sender__email",
        "message",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    inlines = [
        TicketAttachmentInline,
    ]

    ordering = ("-created_at",)

    def short_message(self, obj):

        if len(obj.message) > 50:
            return obj.message[:50] + "..."

        return obj.message

    short_message.short_description = "Message"  # type: ignore

    actions = [
        "reply",
    ]

    # -----------------------------------------
    # Reply View
    # -----------------------------------------

    @admin.action(description="Reply to selected messages")
    def reply(
        self,
        request,
        queryset,
    ):
        updated = 0

        for msg in queryset:
            TicketService.staff_reply(
                message_id=msg.id,
            )
            updated += 1

        self.message_user(
            request,
            f"{updated} tickets replied successfully.",
        )


# ==================================================
# Attachment Admin
# ==================================================


@admin.register(TicketAttachmentModel)
class TicketAttachmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "message",
        "created_at",
    )

    search_fields = ("message__ticket__id",)

    readonly_fields = (
        "id",
        "created_at",
    )
