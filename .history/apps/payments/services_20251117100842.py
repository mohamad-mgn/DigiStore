import uuid
from .models import Payment


class MockPaymentGateway:

    @staticmethod
    def initiate_payment(order, callback_url=None):
        """
        ایجاد رکورد پرداخت و بازگرداندن یک آدرس پرداخت فرضی.
        در پیاده‌سازی واقعی اینجا درخواست به درگاه ارسال می‌شود.
        """
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={'amount': order.total_amount, 'gateway': 'mock'}
        )

        # ساخت شناسه تراکنش موقت
        tx_id = str(uuid.uuid4())
        payment.transaction_id = tx_id
        payment.status = 'initiated'
        payment.save(update_fields=['transaction_id', 'status', 'updated_at'])

        # آدرس فرضی بازگشت (در پروژه واقعی درگاه آن را می‌دهد)
        payment_url = f"/payments/mock-pay/{payment.id}/"
        return payment, payment_url

    @staticmethod
    def verify_payment(payment_id, success=True):
        """
        شبیه‌سازی تایید پرداخت؛ در واقعیت با پارامترهای درگاه چک می‌شود.
        """
        payment = Payment.objects.get(pk=payment_id)
        if success:
            payment.status = 'success'
        else:
            payment.status = 'failed'
        payment.save(update_fields=['status', 'updated_at'])
        return payment