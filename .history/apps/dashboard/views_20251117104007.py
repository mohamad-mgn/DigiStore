from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from apps.orders.models import Order, OrderItem
from apps.product.models import Product
from apps.store.models import Store


# ============================
#   داشبورد خریدار
# ============================

class CustomerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/customer_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        """اگر فروشنده باشد اجازه ورود به داشبورد خریدار ندارد."""
        if request.user.is_seller:
            return redirect("dashboard:seller")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        user = self.request.user

        # آخرین سفارش‌ها
        ctx["orders"] = Order.objects.filter(user=user).order_by("-id")[:10]

        return ctx


# ============================
#   داشبورد فروشنده
# ============================

class SellerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/seller_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        """اگر خریدار باشد نمی‌تواند وارد داشبورد فروشنده شود."""
        if not request.user.is_seller:
            return redirect("dashboard:customer")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        user = self.request.user

        # پیدا کردن فروشگاه فروشنده
        store = Store.objects.filter(seller=user).first()
        ctx["store"] = store

        if store:
            ctx["products"] = store.products.all().order_by("-id")
            ctx["orders"] = OrderItem.objects.filter(product__store=store).order_by("-id")[:10]
        else:
            ctx["products"] = []
            ctx["orders"] = []

        return ctx