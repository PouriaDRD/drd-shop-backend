from django.db import transaction
from django.db.models import QuerySet

from finance.enums import TransactionStatus
from finance.models import RefundToWalletRequestModel, TransactionModel


class RefundToWalletRepository:
    """
    Repository layer for refund to wallet persistence.

    Responsible only for database operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        **kwargs,
    ) -> RefundToWalletRequestModel:
        """
        Create a new refund to wallet request.
        """

        return RefundToWalletRequestModel.objects.create(**kwargs)

    @staticmethod
    def get_by_id(refund_id) -> RefundToWalletRequestModel | None:
        """
        Retrieve refund to wallet by id.
        """

        return (
            RefundToWalletRequestModel.objects.select_related(
                "transaction",
                "transaction__wallet",
            )
            .filter(id=refund_id)
            .first()
        )

    @staticmethod
    def get_by_user(user_id) -> QuerySet[RefundToWalletRequestModel]:
        """
        Retrieve refund to wallet requests for a user.
        """

        return (
            RefundToWalletRequestModel.objects.filter(
                transaction__wallet__user_id=user_id,
            )
            .select_related(
                "transaction",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def lock(
        refund_id,
    ) -> RefundToWalletRequestModel:
        """
        Lock refund row.

        Must be called inside an atomic transaction.
        """

        return (
            RefundToWalletRequestModel.objects.select_for_update()
            .select_related(
                "transaction",
                "transaction__wallet",
            )
            .get(id=refund_id)
        )

    @staticmethod
    @transaction.atomic
    def approve(
        refund: RefundToWalletRequestModel,
    ) -> RefundToWalletRequestModel:
        """
        Approve refund request.
        """

        refund.status = TransactionStatus.APPROVED
        refund.is_processed = True

        refund.save(
            update_fields=[
                "status",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        return refund

    @staticmethod
    @transaction.atomic
    def reject(
        refund: RefundToWalletRequestModel,
        admin_note: str = "",
    ) -> RefundToWalletRequestModel:
        """
        Reject refund request.
        """

        refund.status = TransactionStatus.REJECTED
        refund.is_processed = True
        refund.admin_note = admin_note

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

    @staticmethod
    @transaction.atomic
    def attach_transaction(
        refund: RefundToWalletRequestModel,
        transaction: TransactionModel,
    ) -> RefundToWalletRequestModel:
        """
        Attach parent transaction.
        """

        refund.transaction = transaction

        refund.save(
            update_fields=[
                "transaction",
                "updated_at",
            ]
        )

        return refund
