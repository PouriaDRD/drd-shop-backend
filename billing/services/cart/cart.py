from django.db import transaction
from accounts.models import UserModel
from rest_framework.exceptions import ValidationError

from commerce.services.coupon import CouponService
from commerce.models import ProductModel, ProductPlanModel, CouponModel

from billing.models import CartModel, CartItemModel
from billing.repositories.cart import CartRepository, CartItemRepository


class CartService:
    """
    Business logic for cart.
    """

    @staticmethod
    def get_or_create_cart(user: UserModel):
        return CartRepository.get_or_create(user)

    @staticmethod
    @transaction.atomic
    def add_item(
        user: UserModel, *, product: ProductModel, plan: ProductPlanModel, quantity=1
    ):
        cart = CartService.get_or_create_cart(user)

        if not product.is_active:
            raise ValidationError("محصول غیر فعال است.")

        if not plan.is_active:
            raise ValidationError("پلن غیر فعال است.")

        if not plan.is_available:
            raise ValidationError("پلن موجود نیست.")

        item, created = cart.items.get_or_create(  # type: ignore
            product=product,
            plan=plan,
            defaults={
                "quantity": quantity,
                "unit_price": plan.price,
                "total_price": plan.price * quantity,
            },
        )

        if not created:
            item.quantity += quantity
            item.total_price = item.quantity * item.unit_price
            item.save()

        CartService.recalculate(cart)

        return cart, item

    @staticmethod
    @transaction.atomic
    def update_item(item: CartItemModel, *, quantity: int):
        item.quantity = quantity
        item.total_price = item.unit_price * quantity
        item.save()

        new_cart = CartService.recalculate(item.cart)

        if new_cart.total_price <= 0:
            CartRepository.reset_cart(new_cart)
            return item

        return item

    @staticmethod
    @transaction.atomic
    def remove_item(item: CartItemModel):
        cart = item.cart

        CartItemRepository.delete(item)
        new_cart = CartService.recalculate(cart)

        if new_cart.total_price <= 0:
            CartRepository.reset_cart(new_cart)

        return True

    @staticmethod
    def recalculate(cart: CartModel):
        items = cart.items.all()  # type: ignore

        subtotal = sum(i.total_price for i in items)

        discount = 0

        if cart.coupon:
            discount = CouponService.calculate_discount(
                cart.coupon,
                subtotal,
            )

        cart.subtotal = subtotal
        cart.discount = discount
        cart.total_price = max(subtotal - discount, 0)

        new_cart = CartRepository.save(cart)

        return new_cart

    @staticmethod
    @transaction.atomic
    def add_coupon_to_cart(cart: CartModel, coupon: CouponModel, user_id):
        discount = CouponService.calculate_discount(
            coupon=coupon, subtotal=cart.subtotal, user_id=user_id
        )

        if discount > 0:
            cart.coupon = coupon
            cart.save(update_fields=["coupon"])
            new_cart = CartService.recalculate(cart)
            return new_cart
