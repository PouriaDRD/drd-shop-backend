from django.db import transaction
from finance.models import TransactionModel, WalletModel
from finance.enums import TransactionType, TransactionStatus, PaymentMethod


class TransactionRepository:
    """Repository for TransactionModel."""

    @staticmethod
    @transaction.atomic
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

    @staticmethod
    def update_status(transaction: TransactionModel, status: TransactionStatus):
        transaction.status = status
        transaction.save(update_fields=["status"])

    @staticmethod
    def get_transaction_by_id(id):
        transaction = TransactionModel.objects.get(id=id)
        return transaction

    @staticmethod
    def get_wallet_transactions(id):
        transactions = TransactionModel.objects.filter(wallet_id=id)
        return transactions
