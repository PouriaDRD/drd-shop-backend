from django.db import transaction
from accounts.models import UserModel
from finance.models import WalletModel


class WalletRepository:
    """Repository for WalletModel."""

    @staticmethod
    @transaction.atomic
    def create(user: UserModel):
        wallet = WalletModel.objects.create(user=user)
        return wallet

    @staticmethod
    def get_wallet_by_user_id(id):
        wallet = WalletModel.objects.select_related("user").get(user_id=id)
        return wallet

    @staticmethod
    def get_balance(wallet: WalletModel):
        result = wallet.ledger_entries.aggregate(balance=Sum("amount"))  # type: ignore

        return int(result["balance"]) if result else 0
