from apps.cart.models import Cart
from apps.store.models import Store

def global_context(request):
    """
    بر می‌گرداند:
      - cart_item_count: تعداد آیتم‌های سبد برای کاربر لاگین‌شده (در غیر اینصورت 0)
      - is_authenticated: True/False
      - is_seller: آیا کاربر فروشنده است
      - store_exists: آیا فروشنده فروشگاه دارد (برای نمایش لینک مدیریت فروشگاه)
      - user_name: نام نمایش داده‌شده
    """
    user = getattr(request, "user", None)
    cart_item_count = 0
    is_seller = False
    store_exists = False
    user_name = None

    if user and user.is_authenticated:
        is_seller = getattr(user, "is_seller", False)
        user_name = getattr(user, "full_name", None) or user.phone

        # سعی می‌کنیم سبد را بخوانیم؛ اگر نداشتیم، 0
        try:
            cart = Cart.objects.filter(user=user).first()
            if cart:
                cart_item_count = cart.items.count()
        except Exception:
            cart_item_count = 0

        # برای فروشنده بررسی می‌کنیم آیا فروشگاه ثبت شده دارد
        if is_seller:
            try:
                store_exists = Store.objects.filter(seller=user).exists()
            except Exception:
                store_exists = False

    return {
        "cart_item_count": cart_item_count,
        "is_authenticated": user.is_authenticated if user else False,
        "is_seller": is_seller,
        "store_exists": store_exists,
        "user_name": user_name,
    }