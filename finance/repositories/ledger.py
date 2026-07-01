from django.db import transaction

from finance.enums import TransactionType
from finance.models import LedgerEntryModel, TransactionModel, WalletModel


class LedgerRepository:
    """
    Repository layer for ledger persistence.

    Responsible only for database operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        wallet: WalletModel,
        transaction: TransactionModel,
        transaction_type: TransactionType,
        amount: int,
        balance_before: int,
        balance_after: int,
    ) -> LedgerEntryModel:
        """
        Create a new immutable ledger entry.

        Args:
            wallet: Wallet owner.
            transaction: Parent transaction.
            transaction_type: Financial operation type.
            amount: Signed amount.
            balance_before: Wallet balance before operation.
            balance_after: Wallet balance after operation.

        Returns:
            Newly created LedgerEntryModel.
        """

        return LedgerEntryModel.objects.create(
            wallet=wallet,
            transaction=transaction,
            transaction_type=transaction_type,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
        )

    @staticmethod
    def get_by_id(ledger_id):
        """
        Retrieve ledger entry by id.

        Returns:
            LedgerEntryModel | None
        """

        return (
            LedgerEntryModel.objects.filter(id=ledger_id)
            .select_related(
                "wallet",
                "transaction",
            )
            .first()
        )

    @staticmethod
    def get_wallet_entries(wallet: WalletModel):
        """
        Return wallet ledger history.
        """

        return (
            LedgerEntryModel.objects.filter(wallet=wallet)
            .select_related("transaction")
            .order_by("-created_at")
        )
