from django.db import transaction
from django.utils import timezone
from django.db.models import QuerySet


from finance.models import (
    RefundToWalletRequestModel,
    RefundToUserRequestModel,
)
from finance.enums import (
    RefundToWalletStatus,
    RefundToUserStatus,
)


class RefundRepository:
    """
    Repository layer for refund requests.
    Only DB operations.
    """

    # --------------------------------------------------------
    # WALLET REFUND
    # --------------------------------------------------------
    @staticmethod
    def create_wallet_refund(**kwargs) -> RefundToWalletRequestModel:
        return RefundToWalletRequestModel.objects.create(**kwargs)

    @staticmethod
    def get_wallet_refund_by_id(refund_id):
        return RefundToWalletRequestModel.objects.filter(id=refund_id).first()

    @staticmethod
    def get_wallet_refunds_to_wallet(
        wallet_id: int,
    ) -> QuerySet[RefundToWalletRequestModel]:
        return (
            RefundToWalletRequestModel.objects.filter(wallet_id=wallet_id)
            .select_related(
                "wallet",
                "wallet__user",
                "transaction",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def lock_wallet_refund(refund_id):
        return (
            RefundToWalletRequestModel.objects.select_for_update()
            .select_related("wallet")
            .get(id=refund_id)
        )

    @staticmethod
    @transaction.atomic
    def mark_wallet_refund_approved(refund: RefundToWalletRequestModel):
        refund.status = RefundToWalletStatus.APPROVED
        refund.is_processed = True
        refund.reviewed_at = timezone.now()
        refund.save(
            update_fields=["status", "is_processed", "reviewed_at", "updated_at"]
        )
        return refund

    @staticmethod
    @transaction.atomic
    def mark_wallet_refund_rejected(refund: RefundToWalletRequestModel, note=""):
        refund.status = RefundToWalletStatus.REJECTED
        refund.is_processed = True
        refund.admin_note = note
        refund.reviewed_at = timezone.now()
        refund.save(
            update_fields=[
                "status",
                "admin_note",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )
        return refund

    # --------------------------------------------------------
    # USER REFUND
    # --------------------------------------------------------
    @staticmethod
    def create_user_refund(**kwargs) -> RefundToUserRequestModel:
        return RefundToUserRequestModel.objects.create(**kwargs)

    @staticmethod
    def get_user_refund_by_id(refund_id):
        return RefundToUserRequestModel.objects.filter(id=refund_id).first()

    @staticmethod
    def lock_user_refund(refund_id):
        return (
            RefundToUserRequestModel.objects.select_for_update()
            .select_related("wallet")
            .get(id=refund_id)
        )

    @staticmethod
    @transaction.atomic
    def mark_user_refund_approved(refund: RefundToUserRequestModel):
        refund.status = RefundToUserStatus.APPROVED
        refund.is_processed = True
        refund.reviewed_at = timezone.now()
        refund.save(
            update_fields=["status", "is_processed", "reviewed_at", "updated_at"]
        )
        return refund

    @staticmethod
    @transaction.atomic
    def mark_user_refund_rejected(refund: RefundToUserRequestModel, note=""):
        refund.status = RefundToUserStatus.REJECTED
        refund.is_processed = True
        refund.admin_note = note
        refund.reviewed_at = timezone.now()
        refund.save(
            update_fields=[
                "status",
                "admin_note",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )
        return refund
