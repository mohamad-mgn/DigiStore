from django.urls import reverse
import uuid
from .models import Payment


class MockPaymentGateway:

    @staticmethod
    def initiate_payment(order, callback_url=None):
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={'amount': order.total_amount, 'gateway': 'mock'}
        )

        tx_id = str(uuid.uuid4())
        payment.transaction_id = tx_id
        payment.status = 'initiated'
        payment.save(update_fields=['transaction_id', 'status', 'updated_at'])

        payment_url = reverse("payments:mock", args=[payment.id])
        return payment, payment_url

    @staticmethod
    def verify_payment(payment_id, success=True):
        payment = Payment.objects.get(pk=payment_id)
        payment.status = 'success' if success else 'failed'
        payment.save(update_fields=['status', 'updated_at'])
        return payment