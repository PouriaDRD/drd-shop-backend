from finance.enums import TransactionStatus
from finance.repositories import TransactionRepository


class WalletSelector:
    """Wallet selector."""

    @staticmethod
    def can_deposit(wallet_id: str):
        transactions = TransactionRepository.get_wallet_transactions(id=wallet_id)
        return not transactions.filter(status=TransactionStatus.PENDING).exists()
