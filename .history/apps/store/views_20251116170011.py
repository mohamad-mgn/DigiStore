from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import Store
from .forms import StoreForm


class SellerRequiredMixin(UserPassesTestMixin):
    """فقط کاربرانی که فروشنده هستند اجازه ساخت/ویرایش دارند"""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_seller


# --------------------------
#   لیست همه فروشگاه‌ها
# --------------------------

class StoreListView(ListView):
    model = Store
    template_name = "store/store_list.html"
    context_object_name = "stores"
    paginate_by = 12


# --------------------------
#   صفحه جزئیات فروشگاه
# --------------------------

class StoreDetailView(DetailView):
    model = Store
    template_name = "store/store_detail.html"
    context_object_name = "store"
    slug_field = "slug"
    slug_url_kwarg = "slug"


# --------------------------
#   ایجاد فروشگاه
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
#   ویرایش فروشگاه
# --------------------------

class StoreUpdateView(LoginRequiredMixin, SellerRequiredMixin, UpdateView):
    model = Store
    form_class = StoreForm
    template_name = "store/store_update.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("store:list")

    def get_queryset(self):
        # فقط فروشگاه‌های متعلق به همین فروشنده
        return Store.objects.filter(seller=self.request.user)


# --------------------------
#   حذف فروشگاه
# --------------------------

class StoreDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = Store
    template_name = "store/store_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("store:list")

    def get_queryset(self):
        return Store.objects.filter(seller=self.request.user)