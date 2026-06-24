from finance.models import WalletModel, TransactionModel
from finance.repositories import TransactionRepository, LedgerRepository
from finance.enums import TransactionType, TransactionStatus, PaymentMethod


class RefundService:

    @staticmethod
    def refund(amount: int, wallet: WalletModel, original_tx: TransactionModel):
        """
        Partial or full refund.
        """
        TransactionRepository.update_status(original_tx, TransactionStatus.REFUNDED)

        transaction = TransactionRepository.create(
            amount=amount,
            wallet=wallet,
            type=TransactionType.REFUND,
            status=TransactionStatus.COMPLETED,
            method=PaymentMethod.CARD_TO_CARD,
        )

        LedgerRepository.create(
            amount=-amount,
            wallet=wallet,
            transaction=transaction,
        )

        return transaction
