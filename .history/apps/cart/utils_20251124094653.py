from apps.cart.models import Cart

def get_or_create_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart

    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart