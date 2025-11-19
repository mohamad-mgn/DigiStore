from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from django.http import HttpResponseRedirect

from .models import Order
from .forms import CheckoutForm
from .services import OrderService
from apps.store.models import Store

class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/user_orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related("user").prefetch_related(
            "items__product__category",
            "items__product__store"
        ).order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "orders/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("orders:user_orders")

    def form_valid(self, form):
        user = self.request.user
        address = form.cleaned_data.get('address')
        postal_code = form.cleaned_data.get('postal_code')

        try:
            order = OrderService.create_order_from_cart(
                user,
                address=address,
                postal_code=postal_code
            )
        except ValueError as e:
            messages.error(self.request, str(e))
            return redirect('cart:detail')

        return redirect('orders:detail', pk=order.id)
    

class SellerOrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = "orders/seller_orders.html"
    context_object_name = "orders"
    paginate_by = 15

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller

    def get_queryset(self):
        seller_store = Store.objects.filter(seller=self.request.user).first()
        if not seller_store:
            return Order.objects.none()

        return Order.objects.filter(items__product__store=seller_store).distinct().order_by('-created_at')


class SellerUpdateOrderStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save(update_fields=['status', 'updated_at'])
            messages.success(request, "وضعیت سفارش با موفقیت به‌روز شد.")
        else:
            messages.error(request, "وضعیت نامعتبر است.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('orders:seller_orders')))