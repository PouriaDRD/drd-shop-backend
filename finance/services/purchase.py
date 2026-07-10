import logging

from django.db import transaction
from rest_framework.exceptions import ValidationError

from accounts.repositories import UserRepository
from billing.services.order import OrderService


from notifications.tasks import send_email_task
from notifications.services import NotificationService

from finance.models import PurchaseRequestModel
from finance.enums import TransactionType, TransactionStatus
from finance.repositories import PurchaseRepository, WalletRepository

from .refund import RefundService
from .ledger import LedgerService
from .transaction import TransactionService

logger = logging.getLogger("finance.purchase_service")


class PurchaseService:
    """
    Business logic for purchase flow.

    Flow:
        Lock purchase
            ↓
        Lock wallet
            ↓
        Check balance
            ↓
        Create transaction (PENDING or APPROVED depending system)
            ↓
        Deduct wallet
            ↓
        Create ledger entry (negative amount)
            ↓
        Approve purchase
    """

    @staticmethod
    @transaction.atomic
    def create(**validated_data) -> PurchaseRequestModel:
        """
        Create purchase request.
        """

        wallet = validated_data["wallet"]
        amount = int(validated_data["amount"])
        reason = validated_data.get("reason", "تراکنش خرید")

        if wallet.balance < amount:
            raise ValidationError("موجودی کافی نیست")

        transaction_obj = TransactionService.create(
            wallet=wallet,
            amount=amount,
            transaction_type=TransactionType.PURCHASE,
            status=TransactionStatus.PENDING,
            description=reason,
        )

        LedgerService.create(
            wallet=wallet,
            transaction=transaction_obj,
            transaction_type=TransactionType.PURCHASE,
            amount=-amount,
        )

        validated_data["transaction"] = transaction_obj

        purchase = PurchaseRepository.create(**validated_data)

        PurchaseService.alert_admin(purchase)

        logger.info(
            f"Purchase request created: id={str(purchase.id)}, user={str(wallet.user)}, amount={purchase.amount}",
        )

        return purchase

    @staticmethod
    def get_purchase_statistics(
        wallet_id: str,
    ):

        return {
            "total_purchase_amount": PurchaseRepository.get_total_purchase_amount(
                wallet_id
            ),
            "last_30_days_purchase_amount": PurchaseRepository.get_last_30_days_purchase_amount(
                wallet_id
            ),
        }

    @staticmethod
    @transaction.atomic
    def approve(purchase_id: str) -> PurchaseRequestModel:
        """
        Approve purchase and deduct wallet balance.
        """

        purchase = PurchaseRepository.lock(purchase_id)

        if purchase.is_processed:
            raise ValidationError("Purchase request has already been processed.")

        PurchaseRepository.approve(purchase)

        if purchase.transaction:
            TransactionService.approve(str(purchase.transaction.id))

        OrderService.approve(str(purchase.order.id))

        logger.info(
            f"Purchase approved: id={str(purchase.id)}, user={str(purchase.wallet.user)}, amount={purchase.amount}",
        )

        return purchase

    @staticmethod
    @transaction.atomic
    def reject(purchase_id: str, *, admin_note: str = "") -> PurchaseRequestModel:
        """
        Reject purchase request.
        """

        purchase = PurchaseRepository.lock(purchase_id)

        if purchase.is_processed:
            raise ValidationError("Purchase request has already been processed.")

        wallet = WalletRepository.lock(purchase.wallet.id)
        amount = purchase.amount
        refund_reason = "استرداد به دلیل رد تراکنش خرید"

        refund = RefundService.create_wallet_refund(
            wallet=wallet,
            amount=amount,
            reason=refund_reason,
        )

        RefundService.approve_wallet_refund(str(refund.id), purchase.transaction)

        PurchaseRepository.reject(purchase, admin_note)

        OrderService.reject(str(purchase.order.id))

        logger.info(
            f"Purchase rejected | id={str(purchase.id)}, user={str(purchase.wallet.user)}, amount={purchase.amount}",
        )

        return purchase

    @staticmethod
    def alert_admin(purchase: PurchaseRequestModel):
        """
        Send admin notification for purchase approval.
        """

        admin_user = UserRepository.get_admin_user()

        if not admin_user:
            return

        wallet = purchase.wallet

        NotificationService.create_success(
            user=admin_user,
            title="تراکنش خرید جدید ثبت شد!",
            message=(
                f"تراکنش خرید برای کیف پول شما ثبت شد."
                f"مبلغ: {purchase.amount}\n"
                f"سفارش: {str(purchase.order.id)}\n"
                f"کاربر: {wallet.user}\n"
            ),
        )

        send_email_task.delay(
            template_slug="admin-purchase-alert",
            recipient_email=admin_user.email,
            recipient_name=str(admin_user),
            context={
                "user_email": wallet.user.email,
                "total_amount": purchase.amount,
                "order_id": str(purchase.order.id),
                "order_status": purchase.order.status,
                "site_name": "DRD Shop",
            },
        )  # type: ignore


# {{ site_name }}

# {{ user_email }}

# {{ order_id }}

# {{ order_status }}

# {{ total_amount }}
