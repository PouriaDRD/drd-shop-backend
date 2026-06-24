from finance.models import LedgerEntryModel, TransactionModel, WalletModel


class LedgerRepository:

    @staticmethod
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
