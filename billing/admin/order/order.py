from django.contrib import admin
from django.utils.html import format_html

from billing.models import OrderModel
from billing.enums import OrderStatus
from .order_item import OrderItemInline

DEV = False


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)

    list_display = (
        "user",
        "status_badge",
        "total_price_display",
        "updated_at",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__email",
    )

    autocomplete_fields = ("user",)

    readonly_fields = (
        "id",
        "updated_at",
        "created_at",
    )

    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return DEV

    def has_change_permission(self, request, obj=None):
        return DEV

    def has_delete_permission(self, request, obj=None):
        return DEV

    # ---------------------------------------------------
    # STATUS BADGE
    # ---------------------------------------------------
    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        colors = {
            OrderStatus.PENDING: ("#FEF3C7", "#92400E"),
            OrderStatus.PAID: ("#DCFCE7", "#166534"),
            OrderStatus.FAILED: ("#FEE2E2", "#991B1B"),
            OrderStatus.CANCELED: ("#F3F4F6", "#4B5563"),
        }

        bg, fg = colors.get(obj.status, ("#F3F4F6", "#374151"))

        return format_html(
            """
            <span style="
                background:{};
                color:{};
                padding:4px 10px;
                border-radius:999px;
                font-size:11px;
                font-weight:600;
                display:inline-block;
                line-height:1.2;
            ">
                {}
            </span>
            """,
            bg,
            fg,
            obj.get_status_display(),
        )

    # ---------------------------------------------------
    # PRICE DISPLAY
    # ---------------------------------------------------
    @admin.display(description="Total Price", ordering="total_price")
    def total_price_display(self, obj):
        if obj.total_price is None:
            return "-"

        amount = f"{obj.total_price:,.0f}"

        return format_html(
            "<span>{}</span>",
            amount,
        )
