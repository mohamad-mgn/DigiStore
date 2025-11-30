from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.product.models import Product
from apps.cart.models import Cart, CartItem

class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_pk):
        product = get_object_or_404(Product, pk=product_pk)
        qty = int(request.POST.get('quantity', 1))
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += qty
        else:
            item.quantity = qty
        item.save()
        messages.success(request, "محصول به سبد اضافه شد.")
        return redirect('cart:cart_view')

class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart_view.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        ctx['cart'] = cart
        ctx['items'] = cart.items.all()
        total = sum([it.product.price * it.quantity for it in ctx['items']])
        ctx['total'] = total
        return ctx

class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_pk):
        item = get_object_or_404(CartItem, pk=item_pk, cart__user=request.user)
        qty = int(request.POST.get('quantity', 1))
        if qty <= 0:
            item.delete()
        else:
            item.quantity = qty
            item.save()
        return redirect('cart:cart_view')

class RemoveCartItemView(LoginRequiredMixin, View):
    def post(self, request, item_pk):
        item = get_object_or_404(CartItem, pk=item_pk, cart__user=request.user)
        item.delete()
        return redirect('cart:cart_view')