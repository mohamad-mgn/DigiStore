import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from apps.account.services.otp_service import OTPService
from apps.user.models import User, CustomerProfile, SellerProfile
from .forms import (
    SendOTPForm, VerifyOTPForm, SignupForm,
    SigninForm, EditCustomerProfileForm, EditSellerProfileForm
)
from .models import MobileOTP


# ارسال OTP و چاپ یا ارسال پیامک
def send_otp_view(request):
    if request.method == "POST":
        form = SendOTPForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            OTPService.send_otp(phone)
            return redirect("account:verify_otp", phone=phone)
    else:
        form = SendOTPForm()
    return render(request, "account/send_otp.html", {"form": form})


# تایید OTP با استفاده از OTPService و پیام‌رسانی مناسب
def verify_otp_view(request, phone):
    if request.method == "POST":
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
    else:
        form = VerifyOTPForm(initial={"phone": phone})
    return render(request, "account/verify_otp.html", {"form": form, "phone": phone})


# ثبت‌نام نهایی کاربر 
def signup_view(request, phone):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            role = form.cleaned_data["role"]

            user = User.objects.create(
                phone=phone,
                full_name=full_name,
                is_seller=(role == "seller"),
            )

            # ساخت پروفایل مناسب
            if role == "customer":
                CustomerProfile.objects.update_or_create(user=user)
            else:
                SellerProfile.objects.update_or_create(user=user)

            login(request, user)
            return redirect("home:index")
    else:
        form = SignupForm(initial={"phone": phone})

    return render(request, "account/signup.html", {"form": form, "phone": phone})


# ورود و ارسال OTP مجدد به شماره موبایل
def signin_view(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]

            user = User.objects.filter(phone=phone).first()
            if not user:
                messages.error(request, "این شماره ثبت نشده است.")
                return redirect("account:signin")

            OTPService.send_otp(phone)
            return redirect("account:verify_otp", phone=phone)

    else:
        form = SigninForm()

    return render(request, "account/signin.html", {"form": form})


# خروج از حساب کاربری
def signout_view(request):
    logout(request)
    return redirect("account:signin")


# نمایش پروفایل کاربر
@login_required
def profile_view(request):
    user = request.user
    profile = user.seller_profile if user.is_seller else user.customer_profile

    return render(request, "account/profile_view.html", {
        "user": user,
        "profile": profile
    })


# ویرایش پروفایل (فاقد خطا و تایید دسترسی)
@login_required
def profile_edit_view(request):
    user = request.user

    if user.is_seller:
        profile = user.seller_profile
        form_class = EditSellerProfileForm
        template = "account/profile_edit_seller.html"
    else:
        profile = user.customer_profile
        form_class = EditCustomerProfileForm
        template = "account/profile_edit_customer.html"

    if request.method == "POST":
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save(user=user)
            messages.success(request, "پروفایل ذخیره شد.")
            return redirect("account:profile")
    else:
        form = form_class(instance=profile, initial={"full_name": user.full_name})

    return render(request, template, {"form": form})
