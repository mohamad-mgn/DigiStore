from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.product.models import Product
from .models import Cart, CartItem

def _get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def add_to_cart(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    qty = int(request.POST.get('quantity', 1))
    cart = _get_or_create_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += qty
    else:
        item.quantity = qty
    item.save()
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = _get_or_create_cart(request.user)
    return render(request, 'cart/detail.html', {'cart': cart})

@login_required
def remove_item(request, item_pk):
    item = get_object_or_404(CartItem, pk=item_pk, cart__user=request.user)
    item.delete()
    return redirect('cart:cart_detail')