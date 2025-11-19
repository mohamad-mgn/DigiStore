from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from apps.orders.models import Order

class PaymentView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        return render(request, 'payments/pay.html', {'order': order})

    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        # اینجا می‌توانی درگاه واقعی متصل کنی؛ فعلاً شبیه‌سازی می‌کنیم:
        order.is_paid = True
        order.save()
        messages.success(request, "پرداخت با موفقیت انجام شد.")
        return redirect('orders:detail', pk=order.pk)