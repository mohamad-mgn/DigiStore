from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages

from apps.orders.models import Order, OrderItem
from apps.cart.models import Cart, CartItem

class OrderListView(LoginRequiredMixin, ListView):
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = []  # اطلاعات سفارش از سبد گرفته می‌شود
    template_name = "orders/order_create.html"
    success_url = reverse_lazy('orders:list')

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        items = cart.items.all()
        if not items:
            messages.error(request, "سبد خرید شما خالی است.")
            return redirect('cart:cart_view')

        # ساخت سفارش
        order = Order.objects.create(user=request.user, total_amount=sum([it.product.price * it.quantity for it in items]))
        for it in items:
            OrderItem.objects.create(order=order, product=it.product, quantity=it.quantity, price=it.product.price)
        # پاک کردن سبد
        cart.items.all().delete()
        messages.success(request, "سفارش با موفقیت ثبت شد. برای پرداخت ادامه دهید.")
        return redirect('payments:pay', order_id=order.pk)