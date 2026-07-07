from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.db.models import QuerySet, Sum

from finance.enums import PurchaseStatus
from finance.models import PurchaseRequestModel


class PurchaseRepository:
    """
    Repository layer for purchase requests.

    Only handles DB operations.
    """

    @staticmethod
    @transaction.atomic
    def create(**kwargs) -> PurchaseRequestModel:
        """
        Create purchase request.
        """

        return PurchaseRequestModel.objects.create(**kwargs)

    @staticmethod
    def get_by_id(purchase_id) -> PurchaseRequestModel | None:
        """
        Retrieve purchase by id.
        """

        return (
            PurchaseRequestModel.objects.select_related(
                "transaction",
                "transaction__wallet",
            )
            .filter(id=purchase_id)
            .first()
        )

    @staticmethod
    def get_total_purchase_amount(
        wallet_id: str,
    ) -> int:
        """
        Get total approved purchase amount.
        """

        result = PurchaseRequestModel.objects.filter(
            wallet_id=wallet_id,
            status=PurchaseStatus.APPROVED,
        ).aggregate(total=Sum("amount"))

        return result["total"] or 0

    @staticmethod
    def get_last_30_days_purchase_amount(
        wallet_id: str,
    ) -> int:
        """
        Get purchase amount in last 30 days.
        """

        start_date = timezone.now() - timedelta(days=30)

        result = PurchaseRequestModel.objects.filter(
            wallet_id=wallet_id,
            status=PurchaseStatus.APPROVED,
            created_at__gte=start_date,
        ).aggregate(total=Sum("amount"))

        return result["total"] or 0

    @staticmethod
    def get_wallet_purchases(wallet_id) -> QuerySet[PurchaseRequestModel]:
        """
        Get all purchases for wallet.
        """

        return (
            PurchaseRequestModel.objects.filter(transaction__wallet_id=wallet_id)
            .select_related("transaction")
            .order_by("-created_at")
        )

    @staticmethod
    def lock(purchase_id: str) -> PurchaseRequestModel:
        """
        Lock purchase row.

        Must be used inside atomic transaction.
        """

        return (
            PurchaseRequestModel.objects.select_for_update()
            .select_related(
                "transaction",
                "transaction__wallet",
            )
            .get(id=purchase_id)
        )

    @staticmethod
    @transaction.atomic
    def approve(
        purchase: PurchaseRequestModel,
    ) -> PurchaseRequestModel:
        """
        Mark purchase as approved.
        """

        purchase.is_processed = True
        purchase.reviewed_at = timezone.now()
        purchase.status = PurchaseStatus.APPROVED

        purchase.save(
            update_fields=[
                "status",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        return purchase

    @staticmethod
    @transaction.atomic
    def reject(
        purchase: PurchaseRequestModel,
        admin_note: str = "",
    ) -> PurchaseRequestModel:
        """
        Mark purchase as rejected.
        """

        purchase.is_processed = True
        purchase.admin_note = admin_note
        purchase.reviewed_at = timezone.now()
        purchase.status = PurchaseStatus.REJECTED

        purchase.save(
            update_fields=[
                "status",
                "admin_note",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        return purchase

    @staticmethod
    @transaction.atomic
    def attach_transaction(
        purchase: PurchaseRequestModel,
        transaction_obj,
    ) -> PurchaseRequestModel:
        """
        Attach transaction to purchase.
        """

        purchase.transaction = transaction_obj

        purchase.save(
            update_fields=[
                "transaction",
                "updated_at",
            ]
        )

        return purchase
