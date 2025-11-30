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
        qs = Product.objects.select_related("store", "category").all()

        # Filter by product title (search query)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(title__icontains=q)

        # Filter by category slug
        slug = self.kwargs.get("slug")
        if slug:
            qs = qs.filter(category__slug=slug)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["current_category"] = None

        slug = self.kwargs.get("slug")
        if slug:
            ctx["current_category"] = Category.objects.filter(slug=slug).first()

        return ctx


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_create.html"

    # Ensure that only authenticated sellers can create products
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller

    # Automatically assign the product to the current seller's store
    def form_valid(self, form):
        store = get_object_or_404(Store, seller=self.request.user)
        form.instance.store = store
        return super().form_valid(form)

    # Redirect to the product detail page after successful creation
    def get_success_url(self):
        return self.object.get_absolute_url()


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_update.html"

    # Ensure that only authenticated sellers can update products
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller

    # Limit queryset to products owned by the current seller
    def get_queryset(self):
        return Product.objects.filter(store__seller=self.request.user).select_related("category")

    # Redirect to the product detail page after successful update
    def get_success_url(self):
        return self.object.get_absolute_url()


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "product/product_delete.html"

    # Ensure that only authenticated sellers can delete products
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller

    # Limit queryset to products owned by the current seller
    def get_queryset(self):
        return Product.objects.filter(store__seller=self.request.user)
    
    # Redirect to the product list page after deletion
    def get_success_url(self):
        return reverse_lazy("product:list")


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"

    # Add related products to the context (same category, excluding current product)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["related_products"] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return ctx
    

class ProductSearchView(ListView):
    # Search products by title or description.
    model = Product
    template_name = "product/product_search_results.html"
    context_object_name = "products"

    def get_queryset(self):
        # Return products that contain the search query.
        # Uses __icontains for case-insensitive matching.
        query = self.request.GET.get("q", "")
        return Product.objects.filter(title__icontains=query).select_related("category", "store")
    
    def get_context_data(self, **kwargs):
        # Pass the search query to the template so it can be displayed in results.
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context