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


# ========================================================
# Customer's order list view
# ========================================================
class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "orders/user_orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        # Return all orders for the logged-in user
        # Includes related user, product, category, and store to optimize queries
        return Order.objects.filter(user=self.request.user).select_related("user").prefetch_related(
            "items__product__category",
            "items__product__store"
        ).order_by('-created_at')


# ========================================================
# Customer's order detail view
# ========================================================
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        # Restrict access to orders owned by the logged-in user
        return Order.objects.filter(user=self.request.user)


# ========================================================
# Checkout view for creating a new order from the cart
# ========================================================
class CheckoutView(LoginRequiredMixin, FormView):
    template_name = "orders/checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("orders:user_orders")

    def form_valid(self, form):
        user = self.request.user
        address = form.cleaned_data.get('address')
        postal_code = form.cleaned_data.get('postal_code')

        try:
            # Create order from user's cart
            order = OrderService.create_order_from_cart(
                user,
                address=address,
                postal_code=postal_code
            )
        except ValueError as e:
            # Display error if cart is empty or stock is insufficient
            messages.error(self.request, str(e))
            return redirect('cart:detail')

        # Redirect to order detail page upon successful creation
        return redirect('orders:detail', pk=order.id)
    

# ========================================================
# Seller's order list view
# ========================================================
class SellerOrderListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = "orders/seller_orders.html"
    context_object_name = "orders"
    paginate_by = 15

    def test_func(self):
        # Allow access only to authenticated sellers
        return self.request.user.is_authenticated and self.request.user.is_seller

    def get_queryset(self):
        # Get the store of the logged-in seller
        seller_store = Store.objects.filter(seller=self.request.user).first()
        if not seller_store:
            return Order.objects.none()

        # Return distinct orders containing products from the seller's store
        return Order.objects.filter(items__product__store=seller_store).distinct().order_by('-created_at')


# ========================================================
# Seller's order status update view
# ========================================================
class SellerUpdateOrderStatusView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        # Allow access only to authenticated sellers
        return self.request.user.is_authenticated and self.request.user.is_seller

    def post(self, request, pk):
        # Get the order by ID
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get('status')

        # Validate the new status against allowed choices
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save(update_fields=['status', 'updated_at'])
            messages.success(request, "وضعیت سفارش با موفقیت به‌روز شد.")
        else:
            messages.error(request, "وضعیت نامعتبر است.")

        # Redirect back to the referring page or seller orders page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('orders:seller_orders')))