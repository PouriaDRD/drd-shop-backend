from finance.models import TransactionModel, WalletModel
from finance.utils import TransactionType, TransactionStatus, PaymentMethod


class TransactionRepository:
    """Repository for TransactionModel."""

    @staticmethod
    def create(
        amount: int,
        wallet: WalletModel,
        type: TransactionType = TransactionType.DEPOSIT,
        method: PaymentMethod = PaymentMethod.CARD_TO_CARD,
        status: TransactionStatus = TransactionStatus.PENDING,
        **kwargs
    ):
        new_transaction = TransactionModel.objects.create(
            amount=amount,
            wallet=wallet,
            status=status,
            transaction_type=type,
            payment_method=method,
            **kwargs,
        )
        return new_transaction
