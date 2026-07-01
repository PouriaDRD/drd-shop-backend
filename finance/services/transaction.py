import logging

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from finance.enums import TransactionStatus, TransactionType
from finance.models import TransactionModel, WalletModel
from finance.repositories import TransactionRepository

logger = logging.getLogger("finance.transaction_service")


class TransactionService:
    """
    Business layer for transaction lifecycle.

    This service is responsible only for managing the
    transaction state.

    It DOES NOT modify wallet balances.

    Wallet balance updates are handled by WalletService,
    while immutable accounting records are handled by
    LedgerService.
    """

    @staticmethod
    def create(
        *,
        wallet: WalletModel,
        amount: int,
        transaction_type: TransactionType,
        description: str = "",
    ) -> TransactionModel:
        """
        Create a pending transaction.
        """

        transaction_obj = TransactionRepository.create(
            wallet=wallet,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
        )

        logger.info(
            f"Transaction created | id={transaction_obj.id} wallet={wallet.id} type={transaction_type} amount={amount}"
        )

        return transaction_obj

    @staticmethod
    @transaction.atomic
    def approve(
        transaction_id,
    ) -> TransactionModel:
        """
        Approve a transaction.

        Notes:
            Only changes transaction state.
            Does NOT touch wallet or ledger.
        """

        transaction_obj = TransactionRepository.lock(transaction_id)

        if transaction_obj.is_processed:
            raise ValidationError("Transaction has already been processed.")

        transaction_obj.reviewed_at = timezone.now()

        transaction_obj = TransactionRepository.approve(transaction_obj)

        logger.info(
            f"Transaction approved | id={transaction_obj.id}",
        )

        return transaction_obj

    @staticmethod
    @transaction.atomic
    def reject(
        transaction_id,
    ) -> TransactionModel:
        """
        Reject a transaction.

        Notes:
            No wallet balance changes happen here.
        """

        transaction_obj = TransactionRepository.lock(transaction_id)

        if transaction_obj.is_processed:
            raise ValidationError("Transaction has already been processed.")

        transaction_obj.reviewed_at = timezone.now()

        transaction_obj = TransactionRepository.reject(transaction_obj)

        logger.info(
            f"Transaction rejected | id={transaction_obj.id}",
        )

        return transaction_obj

    @staticmethod
    def ensure_pending(
        transaction_obj: TransactionModel,
    ) -> None:
        """
        Ensure transaction is still pending.
        """

        if transaction_obj.status != TransactionStatus.PENDING:
            raise ValidationError("Transaction is no longer pending.")

    @staticmethod
    def ensure_not_processed(
        transaction_obj: TransactionModel,
    ) -> None:
        """
        Ensure transaction has not been processed before.
        """

        if transaction_obj.is_processed:
            raise ValidationError("Transaction has already been processed.")

    @staticmethod
    def ensure_type(
        transaction_obj: TransactionModel,
        expected_type: TransactionType,
    ) -> None:
        """
        Ensure transaction type matches expected type.
        """

        if transaction_obj.type != expected_type:
            raise ValidationError(f"Expected transaction type '{expected_type}'.")
