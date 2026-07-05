from django.db.models import QuerySet

from accounts.models import UserModel
from shop.models import VPNProvisionedServiceModel


class VPNServiceRepository:
    """
    VPN service database operations.
    """

    @staticmethod
    def get_user_vpn_services(user: UserModel) -> QuerySet[VPNProvisionedServiceModel]:
        """
        Return all VPN services for a specific user.

        Optimized to avoid N+1 queries.
        """

        return (
            VPNProvisionedServiceModel.objects.select_related(
                "order_item",
                "order_item__product",
                "order_item__plan",
            )
            .filter(order_item__order__user=user)
            .order_by("-created_at")
        )
