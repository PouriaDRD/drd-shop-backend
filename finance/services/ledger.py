import logging

from finance.enums import TransactionType
from finance.repositories import LedgerRepository
from finance.models import LedgerEntryModel, TransactionModel, WalletModel

logger = logging.getLogger("finance.ledger_service")


class LedgerService:
    """
    Business layer for immutable ledger operations.

    Every approved financial operation must create exactly one
    ledger entry. Ledger entries are immutable and represent
    the source of truth for wallet balance history.
    """

    @staticmethod
    def create_entry(
        *,
        wallet: WalletModel,
        transaction: TransactionModel,
        transaction_type: TransactionType,
        amount: int,
    ) -> LedgerEntryModel:
        """
        Create a ledger entry for a processed transaction.

        Args:
            wallet: Target wallet.
            transaction: Parent transaction.
            transaction_type: Financial operation type.
            amount: Signed amount.
                Positive values increase balance.
                Negative values decrease balance.

        Returns:
            Created LedgerEntryModel.
        """

        balance_before = wallet.balance
        balance_after = balance_before + amount

        ledger = LedgerRepository.create(
            wallet=wallet,
            transaction=transaction,
            transaction_type=transaction_type,
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_after,
        )

        logger.info(
            (
                "Ledger entry created | "
                f"wallet={wallet.id} transaction={transaction.id} "
                f"type={transaction_type} amount={amount} "
                f"before={balance_before} after={balance_after}"
            )
        )

        return ledger
