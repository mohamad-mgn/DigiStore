from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Product
from .forms import ProductForm
from apps.store.models import Store


class ProductListView(ListView):
    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    paginate_by = 12


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_create.html"

    def form_valid(self, form):
        store = get_object_or_404(Store, seller=self.request.user)
        form.instance.store = store
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("store:my_store")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_update.html"

    def get_queryset(self):
        store = get_object_or_404(Store, seller=self.request.user)
        return Product.objects.filter(store=store)

    def get_success_url(self):
        return reverse_lazy("store:my_store")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product/product_delete.html"

    def get_queryset(self):
        store = get_object_or_404(Store, seller=self.request.user)
        return Product.objects.filter(store=store)

    def get_success_url(self):
        return reverse_lazy("store:my_store")