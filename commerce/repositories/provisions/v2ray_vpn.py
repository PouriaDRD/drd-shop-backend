from django.db.models import QuerySet

from accounts.models import UserModel
from commerce.models import V2rayVPNModel


class V2rayVPNRepository:
    """
    VPN service database operations.
    """

    @staticmethod
    def get_user_vpn_services(user: UserModel) -> QuerySet[V2rayVPNModel]:
        """
        Return all VPN services for a specific user.

        Optimized to avoid N+1 queries.
        """

        return (
            V2rayVPNModel.objects.select_related(
                "order_item",
                "order_item__product",
                "order_item__plan",
            )
            .filter(order_item__order__user=user)
            .order_by("-created_at")
        )
