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
    Add a product to the user's cart.
    - If item exists → increase quantity (only if stock allows)
    - If item doesn't exist → create new CartItem
    - Prevent exceeding available product stock
    """

    def post(self, request, product_id):

        # Fetch user's cart or create one
        cart = get_or_create_cart(request)

        # Fetch product or return 404
        product = get_object_or_404(Product, id=product_id)

        # Try to find an existing cart item for this product
        existing_item = CartItem.objects.filter(cart=cart, product=product).first()

        # --------------------------------------------
        # Case 1: Product already exists in the cart
        # --------------------------------------------
        if existing_item:

            # Prevent increasing beyond available stock
            if existing_item.quantity >= product.stock:
                messages.error(request, "موجودی محصول کافی نیست.")
                return redirect("cart:detail")

            # Increase quantity by 1
            existing_item.quantity += 1
            existing_item.save()

        # --------------------------------------------
        # Case 2: Product NOT in cart yet
        # --------------------------------------------
        else:
            # Product is out of stock
            if product.stock < 1:
                messages.error(request, "این محصول در حال حاضر ناموجود است.")
                return redirect("product:list")

            # Create cart item
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1
            )

        # Success message
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

        if qty > item.product.stock:
            messages.error(request, "موجودی کالا کمتر از این مقدار است.")
            return redirect("cart:detail")

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