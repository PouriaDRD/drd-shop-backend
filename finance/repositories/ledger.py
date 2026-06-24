from django.db import transaction
from finance.models import LedgerEntryModel, TransactionModel, WalletModel


class LedgerRepository:
    """Repository for LedgerEntryModel."""

    @staticmethod
    @transaction.atomic
    def create(
        amount: int,
        wallet: WalletModel,
        transaction: TransactionModel,
        **kwargs,
    ):
        ledger_entry = LedgerEntryModel.objects.create(
            wallet=wallet, transaction=transaction, amount=amount, **kwargs
        )
        return ledger_entry
