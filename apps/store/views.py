from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Store
from .forms import StoreForm


class SellerRequiredMixin(UserPassesTestMixin):
    """Only users who are sellers are allowed to create/edit"""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller


# --------------------------
#   List all stores
# --------------------------

class StoreListView(ListView):
    model = Store
    template_name = "store/store_list.html"
    context_object_name = "stores"
    paginate_by = 12


# --------------------------
#   Store detail page
# --------------------------

class StoreDetailView(DetailView):
    model = Store
    template_name = "store/store_detail.html"
    context_object_name = "store"


# --------------------------
#   Create a new store
# --------------------------

class StoreCreateView(LoginRequiredMixin, SellerRequiredMixin, CreateView):
    model = Store
    form_class = StoreForm
    template_name = "store/store_create.html"
    success_url = reverse_lazy("store:list")

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


# --------------------------
#   Update a store
# --------------------------

class StoreUpdateView(LoginRequiredMixin, SellerRequiredMixin, UpdateView):
    model = Store
    form_class = StoreForm
    template_name = "store/store_update.html"
    success_url = reverse_lazy("store:list")

    def get_queryset(self):
        # Only allow the seller to update their own store
        return Store.objects.filter(seller=self.request.user)


# --------------------------
#   Delete a store
# --------------------------

class StoreDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = Store
    template_name = "store/store_delete.html"
    success_url = reverse_lazy("store:list")

    def get_queryset(self):
        # Only allow the seller to delete their own store
        return Store.objects.filter(seller=self.request.user)