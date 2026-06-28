from django.db import transaction

from accounts.models import UserModel
from finance.repositories import WalletRepository

from .refund import RefundService
from .deposit import DepositService
from .purchase import PurchaseService


class WalletService(DepositService, PurchaseService, RefundService):
    """
    Wallet service.
    """

    @staticmethod
    @transaction.atomic
    def create_wallet(user: UserModel):
        """
        Create a wallet for a user.
        """
        new_wallet = WalletRepository.create(user=user)
        return new_wallet
