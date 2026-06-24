from finance.selectors import WalletSelector
from finance.models import WalletModel, TransactionModel
from finance.repositories import LedgerRepository, TransactionRepository
from finance.enums import (
    PaymentMethod,
    TransactionStatus,
    TransactionType,
)


class DepositService:
    """
    Handle wallet deposit requests.
    """

    @staticmethod
    def request_deposit(
        amount: int,
        wallet: WalletModel,
        method: PaymentMethod = PaymentMethod.CARD_TO_CARD,
        **kwargs,
    ) -> TransactionModel:
        """
        Create deposit request (PENDING).
        """
        can_deposit = WalletSelector.can_deposit(str(wallet.id))

        if not can_deposit:
            raise ValueError("Deposit request already exists")

        transaction = TransactionRepository.create(
            amount=amount,
            wallet=wallet,
            method=method,
            type=TransactionType.DEPOSIT,
            status=TransactionStatus.PENDING,
            **kwargs,
        )

        return transaction

    @staticmethod
    def approve_deposit(transaction: TransactionModel):
        """
        Approve deposit and increase wallet balance via ledger.
        """

        if transaction.status != TransactionStatus.PENDING:
            raise ValueError("Transaction already processed")

        if transaction.transaction_type != TransactionType.DEPOSIT:
            raise ValueError("Invalid transaction type")

        # create ledger entry (REAL MONEY CHANGE)
        LedgerRepository.create(
            amount=transaction.amount,
            wallet=transaction.wallet,
            transaction=transaction,
        )

        TransactionRepository.update_status(transaction, TransactionStatus.COMPLETED)

    @staticmethod
    def reject_deposit(transaction: TransactionModel, admin_user):
        """
        Reject deposit request.
        """

        if transaction.status != TransactionStatus.PENDING:
            raise ValueError("Already processed")

        TransactionRepository.update_status(transaction, TransactionStatus.REJECTED)
