from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from apps.orders.models import Order
from .services import MockPaymentGateway
from .models import Payment


class InitiatePaymentView(LoginRequiredMixin, View):
    """View to start the payment process for an order."""
    
    def get(self, request, order_id):
        # Get the order for the current user
        order = get_object_or_404(Order, id=order_id, user=request.user)

        # If order is already paid, show message and redirect
        if hasattr(order, 'payment') and order.payment.status == 'success':
            messages.info(request, "این سفارش قبلاً پرداخت شده است.")
            return redirect('orders:detail', pk=order.id)

        # Initiate a new payment using the mock gateway
        payment, payment_url = MockPaymentGateway.initiate_payment(order)
        return redirect(payment_url)
    

class MockPaymentPage(View):
    """Simulated payment page for the mock gateway."""
    
    template_name = "payments/mock_payment.html"

    def get(self, request, payment_id):
        # Show the mock payment page
        payment = get_object_or_404(Payment, id=payment_id)
        return render(request, self.template_name, {"payment": payment})

    def post(self, request, payment_id):
        # Handle form submission from mock payment page
        action = request.POST.get('action')
        success = (action == 'success')

        # Update the payment status based on action
        payment = MockPaymentGateway.verify_payment(payment_id, success=success)

        if success:
            # Mark order as paid if payment succeeded
            order = payment.order
            order.status = 'paid'
            order.save(update_fields=['status', 'updated_at'])
            messages.success(request, "پرداخت با موفقیت انجام شد.")
            return redirect('orders:detail', pk=order.id)
        else:
            messages.error(request, "پرداخت ناموفق بود.")
            return redirect('payments:mock', payment_id=payment.id)