from django.urls import reverse
import uuid
from .models import Payment

# ========================================================
# Mock payment gateway for simulating payments
# ========================================================
class MockPaymentGateway:

    @staticmethod
    def initiate_payment(order, callback_url=None):
        """
        Create or get a Payment object for the given order.
        Generate a mock transaction ID and return a payment URL.
        """
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={'amount': order.total_amount, 'gateway': 'mock'}
        )

        # Generate a unique transaction ID
        tx_id = str(uuid.uuid4())
        payment.transaction_id = tx_id
        payment.status = 'initiated'
        payment.save(update_fields=['transaction_id', 'status', 'updated_at'])

        # Generate URL to simulate payment page
        payment_url = reverse("payments:mock", args=[payment.id])
        return payment, payment_url

    @staticmethod
    def verify_payment(payment_id, success=True):
        """
        Mark the payment as success or failed (mock verification).
        """
        payment = Payment.objects.get(pk=payment_id)
        payment.status = 'success' if success else 'failed'
        payment.save(update_fields=['status', 'updated_at'])
        return payment