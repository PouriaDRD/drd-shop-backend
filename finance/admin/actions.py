from django.db import transaction
from django.contrib import messages
from django.http import HttpRequest

from finance.services import WalletService
from finance.enums import TransactionStatus, TransactionType


@transaction.atomic
def approve_deposit(modeladmin, request: HttpRequest, queryset):
    """
    Approve selected deposit transactions.
    """

    for transaction in queryset:
        if transaction.status != TransactionStatus.PENDING:
            continue

        try:
            WalletService.approve_deposit(transaction=transaction)

        except Exception as e:
            messages.error(
                request,
                f"Error: {transaction} - {str(e)}",
            )


@transaction.atomic
def reject_deposit(modeladmin, request: HttpRequest, queryset):

    for transaction in queryset:
        if transaction.status != TransactionStatus.PENDING:
            continue
        WalletService.reject_deposit(transaction=transaction)


@transaction.atomic
def refund_transaction(modeladmin, request: HttpRequest, queryset):

    for transaction in queryset:
        if transaction.status != TransactionStatus.COMPLETED:
            messages.error(request, f"Only completed transactions can be refunded!")
            continue

        if transaction.transaction_type != TransactionType.DEPOSIT:
            messages.error(request, f"Only deposit transactions can be refunded!")
            continue

        WalletService.refund(
            amount=int(transaction.amount),
            wallet=transaction.wallet,
            original_tx=transaction,
        )
