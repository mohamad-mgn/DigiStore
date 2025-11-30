from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .forms import StoreForm
from .models import Store
from apps.product.models import Product


class MyStoreView(LoginRequiredMixin, DetailView):
    template_name = "store/my_store.html"
    context_object_name = "store"

    def get_object(self):
        return get_object_or_404(Store, seller=self.request.user)


class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Store
    form_class = StoreForm
    template_name = "store/store_create.html"

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("store:my_store")


class StoreDetailView(DetailView):
    model = Store
    template_name = "store/store_detail.html"
    context_object_name = "store"


class StoreProductListView(ListView):
    model = Product
    template_name = "store/store_products.html"
    context_object_name = "products"

    def get_queryset(self):
        store_id = self.kwargs["store_id"]
        return Product.objects.filter(store_id=store_id)