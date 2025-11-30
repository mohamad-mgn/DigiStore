from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Store
from apps.user.models import SellerProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.utils.text import slugify
from django.contrib import messages

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'address', 'logo']

class MyStoresView(LoginRequiredMixin, View):
    def get(self, request):
        stores = request.user.seller_profile.stores.all()
        return render(request, 'store/my_stores.html', {'stores': stores})

class StoreCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = StoreForm()
        return render(request, 'store/create_store.html', {'form': form})

    def post(self, request):
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.seller = request.user.seller_profile
            store.slug = slugify(store.name)
            store.save()
            messages.success(request, "فروشگاه ساخته شد.")
            return redirect('store:my_stores')
        return render(request, 'store/create_store.html', {'form': form})

class StoreDetailView(View):
    def get(self, request, slug):
        store = get_object_or_404(Store, slug=slug)
        return render(request, 'store/detail.html', {'store': store})