from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.cart.models import Cart
from .models import Order, OrderItem
from django.urls import reverse

@login_required
def create_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if cart.items.count() == 0:
        return redirect('cart:cart_detail')

    order = Order.objects.create(user=request.user, total_price=0)
    total = 0
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_title=item.product.title,
            product_price=item.product.price,
            quantity=item.quantity
        )
        total += item.product.price * item.quantity
    order.total_price = total
    order.save()
    # پاک کردن آیتم‌ها از سبد
    cart.items.all().delete()
    # هدایت به صفحه پرداخت (mock) با query param
    return redirect(reverse('payments:pay') + f"?order_id={order.pk}")

@login_required
def thankyou(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/thankyou.html', {'order': order})