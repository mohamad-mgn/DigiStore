from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Product
from apps.store.models import Store
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'stock', 'image']

class SellerOwnsStoreMixin(UserPassesTestMixin):
    def test_func(self):
        store_pk = self.kwargs.get('store_pk')
        store = get_object_or_404(Store, pk=store_pk)
        return hasattr(self.request.user, 'seller_profile') and store.seller == self.request.user.seller_profile

class ProductCreateView(LoginRequiredMixin, SellerOwnsStoreMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/create.html"

    def form_valid(self, form):
        store = get_object_or_404(Store, pk=self.kwargs.get('store_pk'))
        form.instance.store = store
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product:product_detail', kwargs={'pk': self.object.pk})

class ProductListView(ListView):
    model = Product
    template_name = "product/list.html"

class ProductDetailView(DetailView):
    model = Product
    template_name = "product/detail.html"