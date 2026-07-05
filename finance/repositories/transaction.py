from django.db import transaction
from django.utils import timezone
from django.db.models import QuerySet
from finance.enums import TransactionStatus, TransactionType
from finance.models import TransactionModel, WalletModel


class TransactionRepository:
    """
    Repository layer for transaction persistence.

    Responsible only for database operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        wallet: WalletModel,
        amount: int,
        transaction_type: TransactionType,
        status: TransactionStatus = TransactionStatus.PENDING,
        description: str = "",
    ) -> TransactionModel:
        """
        Create a transaction.

        Args:
            wallet: Target wallet.
            amount: Signed amount.
            transaction_type: Transaction type.
            description: Optional description.
            status: Initial transaction status.

        Returns:
            Newly created transaction.
        """

        return TransactionModel.objects.create(
            wallet=wallet,
            amount=amount,
            type=transaction_type,
            status=status,
            description=description,
        )

    @staticmethod
    def get_by_id(transaction_id) -> TransactionModel | None:
        """
        Retrieve transaction by id.
        """

        return (
            TransactionModel.objects.select_related("wallet")
            .filter(id=transaction_id)
            .first()
        )

    @staticmethod
    def get_wallet_transactions(
        wallet: WalletModel,
    ) -> QuerySet[TransactionModel]:
        """
        Return wallet transaction history.
        """

        return (
            TransactionModel.objects.filter(wallet=wallet)
            .select_related("wallet")
            .order_by("-created_at")
        )

    @staticmethod
    @transaction.atomic
    def mark_processed(
        transaction_obj: TransactionModel,
        status: TransactionStatus,
    ) -> TransactionModel:
        """
        Mark transaction as processed.

        This method must only be called once.
        """

        transaction_obj.is_processed = True
        transaction_obj.reviewed_at = timezone.now()
        transaction_obj.status = status

        transaction_obj.save(
            update_fields=[
                "status",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        return transaction_obj

    @staticmethod
    @transaction.atomic
    def approve(
        transaction_obj: TransactionModel,
    ) -> TransactionModel:
        """
        Approve transaction.
        """

        TransactionRepository.mark_processed(
            transaction_obj, TransactionStatus.APPROVED
        )

        transaction_obj.save(
            update_fields=[
                "status",
                "reviewed_at",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        return transaction_obj

    @staticmethod
    @transaction.atomic
    def reject(
        transaction_obj: TransactionModel,
    ) -> TransactionModel:
        """
        Reject transaction.
        """

        TransactionRepository.mark_processed(
            transaction_obj, TransactionStatus.REJECTED
        )

        transaction_obj.save(
            update_fields=[
                "status",
                "reviewed_at",
                "is_processed",
                "reviewed_at",
                "updated_at",
            ]
        )

        return transaction_obj

    @staticmethod
    def lock(transaction_id) -> TransactionModel:
        """
        Lock transaction row for update.

        Must be called inside an atomic transaction.
        """

        return TransactionModel.objects.select_for_update().get(
            id=transaction_id,
        )
