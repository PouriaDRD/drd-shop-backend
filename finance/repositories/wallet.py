from finance.models import WalletModel


class WalletRepository:
    """Repository for WalletModel."""

    @staticmethod
    def get_wallet_by_user_id(id):
        wallet = WalletModel.objects.select_related("user").get(user_id=id)
        return wallet

    @staticmethod
    def get_balance(wallet: WalletModel):
        result = wallet.ledger_entries.aggregate(balance=Sum("amount"))  # type: ignore

        return result["balance"] or 0
