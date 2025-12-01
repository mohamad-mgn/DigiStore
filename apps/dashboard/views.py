from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import View

from apps.orders.models import Order, OrderItem
from apps.product.models import Product
from apps.store.models import Store

# ============================
#   Customer Dashboard
# ============================

class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard view for customers.
    Displays the latest 10 orders of the logged-in customer.
    Redirects to seller dashboard if a seller tries to access this page.
    """
    template_name = "dashboard/customer_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_seller:
            return redirect("dashboard:seller")  # Prevent sellers from accessing customer dashboard
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetch last 10 orders of the customer
        ctx["orders"] = (
            Order.objects
            .filter(user=user)
            .order_by("-id")[:10]
        )

        return ctx


# ============================
#   Seller Dashboard
# ============================

class SellerDashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard view for sellers.
    Displays seller's store, products, and recent orders related to their products.
    Redirects to customer dashboard if a non-seller tries to access this page.
    """
    template_name = "dashboard/seller_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_seller:
            return redirect("dashboard:customer")  # Prevent customers from accessing seller dashboard
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetch the seller's store
        store = Store.objects.filter(seller=user).first()
        ctx["store"] = store

        if store:
            # Fetch products belonging to this store
            ctx["products"] = (
                store.products
                .select_related("category")
                .order_by("-id")
            )

            # Fetch last 10 order items related to this store's products
            ctx["orders"] = (
                OrderItem.objects
                .filter(product__store=store)
                .select_related("product", "order")
                .order_by("-id")[:10]
            )
        else:
            ctx["products"] = []
            ctx["orders"] = []

        return ctx

class SellerStockView(View):
    """
    Show and edit stock for seller products.
    """

    def get(self, request):
        products = Product.objects.filter(store__owner=request.user)
        return render(request, "dashboard/seller_stock.html", {
            "products": products
        })

    def post(self, request):
        product_id = request.POST.get("product_id")
        stock = request.POST.get("stock")

        product = Product.objects.filter(
            id=product_id,
            store__owner=request.user
        ).first()

        if not product:
            messages.error(request, "محصول یافت نشد.")
            return redirect("dashboard:seller_stock")

        product.stock = int(stock)
        product.save(update_fields=["stock"])

        messages.success(request, "موجودی با موفقیت بروزرسانی شد.")
        return redirect("dashboard:seller_stock")