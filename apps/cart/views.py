from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from apps.product.models import Product
from .models import Cart, CartItem
from .utils import get_or_create_cart

# --------------------------------------------------------
# Cart Views
# --------------------------------------------------------

class CartView(TemplateView):
    """
    Display the current user's cart and its items.
    """
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        cart = get_or_create_cart(self.request)
        ctx["cart"] = cart
        ctx["items"] = cart.items.select_related("product")  # Optimize queries with select_related
        return ctx


class AddToCartView(View):
    """
    Add a product to the cart or increase its quantity if it already exists.
    """
    def post(self, request, product_id):
        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, id=product_id)

        # ❗ Prevent adding more than available stock
        existing_item = CartItem.objects.filter(cart=cart, product=product).first()

        if existing_item:
            if existing_item.quantity >= product.stock:
                messages.error(request, "موجودی محصول کافی نیست.")
                return redirect("cart:detail")

            existing_item.quantity += 1
            existing_item.save()

        else:
            if product.stock < 1:
                messages.error(request, "این محصول در حال حاضر ناموجود است.")
                return redirect("product:list")

            CartItem.objects.create(cart=cart, product=product, quantity=1)

        messages.success(request, "محصول به سبد خرید اضافه شد.")
        return redirect("cart:detail")


class RemoveFromCartView(View):
    """
    Remove a specific cart item from the cart.
    """
    def post(self, request, item_id):
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()
        return redirect("cart:detail")


class UpdateCartItemView(View):
    """
    Update the quantity of a specific cart item.
    Deletes the item if quantity is zero or negative.
    """
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
    """
    Remove all items from the current user's cart.
    """
    def post(self, request):
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        return redirect("cart:detail")