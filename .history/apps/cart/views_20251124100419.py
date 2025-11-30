from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from apps.product.models import Product
from .models import Cart, CartItem
from .utils import get_or_create_cart


class CartView(TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        ctx["cart"] = cart
        ctx["items"] = cart.items.select_related("product")
        return ctx


class AddToCartView(View):
    def post(self, request, product_id):
        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            item.quantity += 1
            item.save()

        messages.success(request, "محصول به سبد خرید اضافه شد.")
        return redirect("cart:detail")


class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return redirect("cart:detail")


class UpdateCartItemView(View):
    def post(self, request, item_id):
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        qty = int(request.POST.get("quantity", 1))

        if qty <= 0:
            item.delete()
        else:
            item.quantity = qty
            item.save()

        return redirect("cart:detail")


class ClearCartView(View):
    def post(self, request):
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        return redirect("cart:detail")