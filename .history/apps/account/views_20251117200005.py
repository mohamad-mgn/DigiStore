from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from apps.account.services.otp_service import OTPService
from apps.user.models import User, CustomerProfile, SellerProfile
from .forms import (
    SendOTPForm, VerifyOTPForm, SignupForm,
    SigninForm, EditCustomerProfileForm, EditSellerProfileForm
)


class SendOTPView(View):
    template_name = "account/send_otp.html"

    def get(self, request):
        form = SendOTPForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SendOTPForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            OTPService.send_otp(phone)
            return redirect("account:verify_otp", phone=phone)
        return render(request, self.template_name, {"form": form})


class VerifyOTPView(View):
    template_name = "account/verify_otp.html"

    def get(self, request, phone):
        form = VerifyOTPForm(initial={"phone": phone})
        return render(request, self.template_name, {"form": form, "phone": phone})

    def post(self, request, phone):
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            is_valid, msg = OTPService.validate_otp(phone, code)
            if is_valid:
                user = User.objects.filter(phone=phone).first()
                if user:
                    login(request, user)
                    return redirect("home:index")
                return redirect("account:signup", phone=phone)
            messages.error(request, msg)
            return redirect("account:verify_otp", phone=phone)
        return render(request, self.template_name, {"form": form, "phone": phone})


class SignupView(View):
    template_name = "account/signup.html"

    def get(self, request, phone):
        form = SignupForm(initial={"phone": phone})
        return render(request, self.template_name, {"form": form, "phone": phone})

    def post(self, request, phone):
        form = SignupForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            role = form.cleaned_data["role"]

            # فقط کاربر ساخته می‌شود
            user = User.objects.create(
                phone=phone,
                full_name=full_name,
                is_seller=(role == "seller"),
            )

            # پروفایل‌ها به‌صورت خودکار در signals ساخته می‌شوند
            login(request, user)

            return redirect("home:index")

        return render(request, self.template_name, {"form": form, "phone": phone})


class SigninView(View):
    template_name = "account/signin.html"

    def get(self, request):
        form = SigninForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = SigninForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            user = User.objects.filter(phone=phone).first()
            if not user:
                messages.error(request, "این شماره ثبت نشده است.")
                return redirect("account:signin")
            OTPService.send_otp(phone)
            return redirect("account:verify_otp", phone=phone)
        return render(request, self.template_name, {"form": form})


class SignoutView(View):
    def get(self, request):
        logout(request)
        return redirect("account:signin")


class ProfileView(LoginRequiredMixin, View):
    template_name = "account/profile_view.html"

    def get(self, request):
        user = request.user
        profile = user.seller_profile if user.is_seller else user.customer_profile
        return render(request, self.template_name, {
            "user": user,
            "profile": profile
        })


class ProfileEditView(LoginRequiredMixin, View):

    def get_form_and_template(self, user):
        if user.is_seller:
            return EditSellerProfileForm, "account/profile_edit_seller.html", user.seller_profile
        return EditCustomerProfileForm, "account/profile_edit_customer.html", user.customer_profile

    def get(self, request):
        form_class, template, profile = self.get_form_and_template(request.user)
        form = form_class(instance=profile, initial={"full_name": request.user.full_name})
        return render(request, template, {"form": form})

    def post(self, request):
        form_class, template, profile = self.get_form_and_template(request.user)
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, "پروفایل ذخیره شد.")
            return redirect("account:profile")
        return render(request, template, {"form": form})
