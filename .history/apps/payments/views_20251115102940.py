from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order

@login_required
def pay_view(request):
    order_id = request.GET.get('order_id')
    if not order_id:
        return redirect('cart:cart_detail')
    order = get_object_or_404(Order, pk=order_id, user=request.user)

    if request.method == 'POST':
        # شبیه‌سازی موفق پرداخت:
        order.paid = True
        order.save()
        return redirect('orders:thankyou', pk=order.pk)

    return render(request, 'payments/pay.html', {'order': order})