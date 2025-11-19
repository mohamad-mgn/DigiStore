import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from apps.user.models import User, CustomerProfile, SellerProfile
from .forms import (
    SendOTPForm, VerifyOTPForm, SignupForm,
    SigninForm, EditCustomerProfileForm, EditSellerProfileForm
)
from .models import MobileOTP


# ------------------------------------
#   ارسال OTP
# ------------------------------------

def send_otp(phone):
    """ساخت و ذخیره کد OTP و چاپ در کنسول (به‌جای پیامک)"""
    code = random.randint(100000, 999999)

    MobileOTP.objects.update_or_create(
        phone=phone,
        defaults={"code": code}
    )

    print("کد تأیید:", code)
    return code


def send_otp_view(request):
    if request.method == "POST":
        form = SendOTPForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            send_otp(phone)
            return redirect("account:verify_otp", phone=phone)
    else:
        form = SendOTPForm()

    return render(request, "account/send_otp.html", {"form": form})


# ------------------------------------
#   تأیید OTP
# ------------------------------------

def verify_otp_view(request, phone):
    if request.method == "POST":
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]

            try:
                otp = MobileOTP.objects.get(phone=phone)
            except MobileOTP.DoesNotExist:
                messages.error(request, "کد معتبر نیست.")
                return redirect("account:send_otp")

            if otp.is_expired():
                messages.error(request, "کد منقضی شده. دوباره درخواست دهید.")
                return redirect("account:send_otp")

            if str(otp.code) != code:
                otp.increment_attempts()
                messages.error(request, "کد اشتباه است.")
                return redirect("account:verify_otp", phone=phone)

            otp.mark_verified()

            # ورود اگر کاربر از قبل وجود دارد
            user = User.objects.filter(phone=phone).first()
            if user:
                login(request, user)
                return redirect("home:index")

            # اگر وجود نداشت → ثبت‌نام
            return redirect("account:signup", phone=phone)
    else:
        form = VerifyOTPForm(initial={"phone": phone})

    return render(request, "account/verify_otp.html", {"form": form, "phone": phone})


# ------------------------------------
#   ثبت‌نام کامل
# ------------------------------------

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


# ------------------------------------
#   ورود
# ------------------------------------

def signin_view(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]

            user = User.objects.filter(phone=phone).first()

            if not user:
                messages.error(request, "این شماره ثبت نشده است.")
                return redirect("account:signin")

            send_otp(phone)
            return redirect("account:verify_otp", phone=phone)

    else:
        form = SigninForm()

    return render(request, "account/signin.html", {"form": form})


# ------------------------------------
#   خروج
# ------------------------------------

def signout_view(request):
    logout(request)
    return redirect("account:signin")


# ------------------------------------
#   دیدن پروفایل
# ------------------------------------

@login_required
def profile_view(request):
    user = request.user
    profile = user.seller_profile if user.is_seller else user.customer_profile

    return render(request, "account/profile_view.html", {
        "user": user,
        "profile": profile
    })


# ------------------------------------
#   ویرایش پروفایل
# ------------------------------------

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