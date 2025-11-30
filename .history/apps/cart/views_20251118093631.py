from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.product.models import Product
from .models import Cart, CartItem
from django.contrib import messages


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        ctx["cart"] = cart
        ctx["items"] = cart.items.select_related("product")
        return ctx



class AddToCartView(LoginRequiredMixin, View):
    """افزودن یک محصول به سبد خرید"""

    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        item, created_item = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created_item:
            item.quantity += 1
            item.save()

        messages.success(request, "محصول به سبد خرید اضافه شد.")
        return redirect("cart:detail")



class RemoveFromCartView(LoginRequiredMixin, View):
    """حذف کامل یک محصول از سبد"""

    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        messages.info(request, "آیتم حذف شد.")
        return redirect("cart:view")



class UpdateCartItemView(LoginRequiredMixin, View):
    """ویرایش تعداد محصول"""

    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        qty = int(request.POST.get("quantity", 1))

        if qty <= 0:
            item.delete()
        else:
            item.quantity = qty
            item.save()

        messages.success(request, "تعداد به‌روزرسانی شد.")
        return redirect("cart:detail")



class ClearCartView(LoginRequiredMixin, View):
    """خالی کردن کامل سبد"""

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()

        messages.info(request, "سبد خرید خالی شد.")
        return redirect("cart:detail")