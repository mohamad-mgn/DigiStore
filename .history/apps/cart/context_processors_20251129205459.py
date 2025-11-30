from .models import Cart

def cart_info(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            return {
                "cart_count": cart.items.count()
            }
    return {"cart_count": 0}