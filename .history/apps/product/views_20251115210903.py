from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm
from apps.store.models import Store


class ProductListView(ListView):
    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.all().select_related("store", "category")

        q = self.request.GET.get("q")
        category = self.request.GET.get("category")

        if q:
            qs = qs.filter(title__icontains=q)

        if category:
            qs = qs.filter(category_id=category)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"


class SellerRequiredMixin(UserPassesTestMixin):
    """فقط فروشنده اجازه افزودن / ویرایش محصول دارد"""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller


class ProductCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_create.html"
    success_url = reverse_lazy("product:list")

    def form_valid(self, form):
        # پیدا کردن فروشگاه شخص فروشنده
        store = get_object_or_404(Store, seller=self.request.user)
        form.instance.store = store
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, SellerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_update.html"
    success_url = reverse_lazy("product:list")

    def get_queryset(self):
        # فقط محصولات همین فروشنده
        return Product.objects.filter(store__seller=self.request.user)


class ProductDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = Product
    template_name = "product/product_delete.html"
    success_url = reverse_lazy("product:list")

    def get_queryset(self):
        return Product.objects.filter(store__seller=self.request.user)