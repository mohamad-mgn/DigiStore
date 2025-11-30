from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import UpdateView
from django.urls import reverse_lazy

from .forms import UserUpdateForm, CustomerProfileForm, SellerProfileForm
from .models import User


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        context = {"user": user}
        if user.is_seller:
            context["seller_profile"] = user.seller_profile
        context["customer_profile"] = user.customer_profile
        return render(request, "user/profile_view.html", context)


class ProfileEditView(LoginRequiredMixin, View):
    """
    ویرایش پروفایل: ترکیبی از فرم user و فرم پروفایل مربوطه
    """
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        if request.user.is_seller:
            profile_form = SellerProfileForm(instance=request.user.seller_profile)
        else:
            profile_form = CustomerProfileForm(instance=request.user.customer_profile)
        return render(request, "user/profile_edit.html", {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if request.user.is_seller:
            profile_form = SellerProfileForm(request.POST, instance=request.user.seller_profile)
        else:
            profile_form = CustomerProfileForm(request.POST, instance=request.user.customer_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse_lazy("user:profile"))
        return render(request, "user/profile_edit.html", {"user_form": user_form, "profile_form": profile_form})