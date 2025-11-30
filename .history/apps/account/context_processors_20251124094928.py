from apps.cart.models import Cart
from apps.cart.utils import get_or_create_cart
from apps.store.models import Store

def global_context(request):
    user = getattr(request, "user", None)
    cart_item_count = 0
    is_seller = False
    store_exists = False
    user_name = None

    if user and user.is_authenticated:
        is_seller = getattr(user, "is_seller", False)
        user_name = getattr(user, "full_name", None) or user.phone


        try:
            cart = Cart.objects.filter(user=user).first()
            if cart:
                cart_item_count = cart.items.count()
        except Exception:
            cart_item_count = 0

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


def global_context(request):
    cart = get_or_create_cart(request)
    return {
        "cart_items_count": cart.items.count()
    }