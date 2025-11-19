from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from apps.orders.models import Order
from .services import MockPaymentGateway
from .models import Payment


class InitiatePaymentView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if hasattr(order, 'payment') and order.payment.status == 'success':
            messages.info(request, "این سفارش قبلاً پرداخت شده است.")
            return redirect('orders:detail', pk=order.id)

        payment, payment_url = MockPaymentGateway.initiate_payment(order)
        return redirect(payment_url)
    

class MockPaymentPage(View):
    template_name = "payments/mock_payment.html"

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)
        return render(request, self.template_name, {"payment": payment})

    def post(self, request, payment_id):
        action = request.POST.get('action')
        success = (action == 'success')
        payment = MockPaymentGateway.verify_payment(payment_id, success=success)

        if success:
            order = payment.order
            order.status = 'paid'
            order.save(update_fields=['status', 'updated_at'])
            messages.success(request, "پرداخت با موفقیت انجام شد.")
            return redirect('orders:detail', pk=order.id)
        else:
            messages.error(request, "پرداخت ناموفق بود.")
            return redirect('payments:mock', payment_id=payment.id)