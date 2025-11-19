# apps/account/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from apps.user.models import User, CustomerProfile, SellerProfile
from apps.account.models import MobileOTP
from .forms import SignupForm, SigninForm, CustomerProfileForm, SellerProfileForm

import random


def generate_otp():
    return random.randint(100000, 999999)


# ---------------------------------------------------
# Signup (Phone + Name)  → send OTP
# ---------------------------------------------------
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            full_name = form.cleaned_data["full_name"]

            # اگر کاربر وجود ندارد، بساز
            user, created = User.objects.get_or_create(phone=phone)

            if created:
                user.full_name = full_name
                user.save()
                CustomerProfile.objects.create(user=user)

            # OTP
            code = generate_otp()
            MobileOTP.objects.create(phone=phone, code=code)

            request.session["signup_phone"] = phone
            messages.success(request, "OTP sent successfully.")
            return redirect("account:verify")

    else:
        form = SignupForm()

    return render(request, "account/signup.html", {"form": form})


# ---------------------------------------------------
# Signin (Phone Only) → send OTP
# ---------------------------------------------------
def signin_view(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]

            if not User.objects.filter(phone=phone).exists():
                messages.error(request, "Phone number is not registered.")
                return redirect("account:signup")

            code = generate_otp()
            MobileOTP.objects.create(phone=phone, code=code)

            request.session["signup_phone"] = phone
            messages.success(request, "OTP sent.")
            return redirect("account:verify")

    else:
        form = SigninForm()

    return render(request, "account/signin.html", {"form": form})


# ---------------------------------------------------
# Verify OTP
# ---------------------------------------------------
def verify_otp_view(request):
    phone = request.session.get("signup_phone")

    if not phone:
        return redirect("account:signin")

    if request.method == "POST":
        otp_input = request.POST.get("otp")

        otp_obj = MobileOTP.objects.filter(phone=phone).order_by("-created_at").first()

        if otp_obj and otp_obj.code == otp_input:
            user = User.objects.get(phone=phone)
            login(request, user)
            messages.success(request, "You logged in successfully.")
            return redirect("account:profile")

        messages.error(request, "Invalid OTP. Try again.")

    return render(request, "account/verify.html", {"phone": phone})


# ---------------------------------------------------
# Logout
# ---------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect("account:signin")


# ---------------------------------------------------
# Profile Page
# ---------------------------------------------------
@login_required
def profile_view(request):
    user = request.user
    if user.is_seller:
        profile = SellerProfile.objects.get(user=user)
    else:
        profile = CustomerProfile.objects.get(user=user)

    return render(request, "account/profile.html", {"profile": profile})


# ---------------------------------------------------
# Profile Edit
# ---------------------------------------------------
@login_required
def profile_edit_view(request):
    user = request.user

    if user.is_seller:
        profile = SellerProfile.objects.get(user=user)
        form_class = SellerProfileForm
    else:
        profile = CustomerProfile.objects.get(user=user)
        form_class = CustomerProfileForm

    if request.method == "POST":
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("account:profile")
    else:
        form = form_class(instance=profile)

    return render(request, "account/profile_edit.html", {"form": form})