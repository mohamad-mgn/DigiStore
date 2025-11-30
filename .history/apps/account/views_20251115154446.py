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

import random


# ===========================================
#   ارسال کد تأیید (OTP)
# ===========================================

def send_otp(phone):
    """
    ساخت و ذخیره کد تأیید برای شماره موبایل و
    چاپ آن در کنسول (فعلاً به‌جای پیامک)
    """
    code = random.randint(100000, 999999)

    MobileOTP.objects.update_or_create(
        phone=phone,
        defaults={'code': code}
    )

    print("کد تأیید ارسال شد:", code)
    return code


def send_otp_view(request):
    """
    صفحه دریافت شماره موبایل و ارسال OTP
    """
    if request.method == 'POST':
        form = SendOTPForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            send_otp(phone)
            return redirect('account:verify_otp', phone=phone)
    else:
        form = SendOTPForm()

    return render(request, 'account/send_otp.html', {'form': form})


# ===========================================
#   تأیید کد OTP
# ===========================================

def verify_otp_view(request, phone):
    """
    صفحه وارد کردن کد تأیید و اعتبارسنجی آن
    """
    if request.method == 'POST':
        form = VerifyOTPForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']

            try:
                otp = MobileOTP.objects.get(phone=phone)
            except MobileOTP.DoesNotExist:
                messages.error(request, "کد معتبر نیست. دوباره تلاش کنید.")
                return redirect('account:send_otp')

            if str(otp.code) != code:
                messages.error(request, "کد وارد شده اشتباه است.")
                return redirect('account:verify_otp', phone=phone)

            # اگر کاربر وجود دارد → ورود
            user = User.objects.filter(phone=phone).first()
            if user:
                login(request, user)
                return redirect('home:home')

            # اگر کاربر نبود → انتقال به ثبت‌نام
            return redirect('account:signup', phone=phone)
    else:
        form = VerifyOTPForm(initial={'phone': phone})

    return render(request, 'account/verify_otp.html', {'form': form, 'phone': phone})


# ===========================================
#   ثبت‌نام کامل کاربر (انتخاب نقش)
# ===========================================

def signup_view(request, phone):
    """
    صفحه‌ای که کاربر پس از تأیید OTP
    باید نام و نقش خود را وارد کند
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():

            full_name = form.cleaned_data['full_name']
            role = form.cleaned_data['role']

            # ساخت کاربر
            user = User.objects.create(
                phone=phone,
                full_name=full_name,
                is_seller=(role == 'seller'),
            )

            # ساخت پروفایل مناسب نقش
            if role == 'customer':
                CustomerProfile.objects.create(user=user)
            else:
                SellerProfile.objects.create(user=user, store_name="فروشگاه جدید")

            login(request, user)
            return redirect('home:home')

    else:
        form = SignupForm(initial={'phone': phone})

    return render(request, 'account/signup.html', {'form': form, 'phone': phone})


# ===========================================
#   ورود (Signin)
# ===========================================

def signin_view(request):
    """
    صفحه ورود: کاربر شماره موبایل را وارد می‌کند
    """
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']

            user = User.objects.filter(phone=phone).first()
            if not user:
                messages.error(request, "این شماره هنوز ثبت‌نام نشده است.")
                return redirect('account:signin')

            # ارسال OTP برای ورود
            send_otp(phone)
            return redirect('account:verify_otp', phone=phone)
    else:
        form = SigninForm()

    return render(request, 'account/signin.html', {'form': form})


# ===========================================
#   خروج از حساب
# ===========================================

def signout_view(request):
    logout(request)
    return redirect('account:signin')


# ===========================================
#   نمایش پروفایل
# ===========================================

@login_required
def profile_view(request):
    """
    نمایش پروفایل بسته به نقش کاربر
    """
    user = request.user

    profile = user.seller_profile if user.is_seller else user.customer_profile

    return render(request, 'account/profile_view.html', {
        'user': user,
        'profile': profile,
    })


# ===========================================
#   ویرایش پروفایل
# ===========================================

@login_required
def profile_edit_view(request):
    """
    ویرایش پروفایل فروشنده / خریدار
    """
    user = request.user

    if user.is_seller:
        profile = user.seller_profile
        form_class = EditSellerProfileForm
        template = 'account/profile_edit_seller.html'
    else:
        profile = user.customer_profile
        form_class = EditCustomerProfileForm
        template = 'account/profile_edit_customer.html'

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save(user=user)
            messages.success(request, "پروفایل با موفقیت ذخیره شد.")
            return redirect('account:profile')
    else:
        form = form_class(instance=profile, initial={'full_name': user.full_name})

    return render(request, template, {'form': form})