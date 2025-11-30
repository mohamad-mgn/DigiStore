from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import SendOTPForm, VerifyOTPForm, SignupForm, SigninForm
from .models import MobileOTP
from apps.user.models import User
from django.contrib import messages, auth
import random

def send_sms_mock(phone, code):
    """
    ارسال SMS به صورت mock: فقط چاپ در کنسول.
    برای اتصال سرویس واقعی این تابع را تغییر بده.
    """
    print(f"[MOCK SMS] OTP for {phone}: {code}")

class SendOTPView(View):
    template_name = "account/send_otp.html"
    form_class = SendOTPForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            code = f"{random.randint(100000, 999999)}"
            MobileOTP.objects.create(phone=phone, code=code)
            send_sms_mock(phone, code)
            request.session['otp_phone'] = phone
            messages.success(request, "کد برای شماره ارسال شد (mock).")
            return redirect('account:verify_otp')
        return render(request, self.template_name, {'form': form})

class VerifyOTPView(View):
    template_name = "account/verify_otp.html"
    form_class = VerifyOTPForm

    def get(self, request):
        phone = request.session.get('otp_phone', '')
        form = self.form_class(initial={'phone': phone})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            code = form.cleaned_data['code']
            otp = MobileOTP.objects.filter(phone=phone, code=code, verified=False).order_by('-created_at').first()
            if otp:
                otp.verified = True
                otp.save()
                request.session['verified_phone'] = phone
                # اگر کاربر وجود داشت، لاگین کن
                try:
                    user = User.objects.get(phone=phone)
                    auth.login(request, user)
                    messages.success(request, "وارد شدید.")
                    return redirect('account:profile')
                except User.DoesNotExist:
                    return redirect('account:signup')
            messages.error(request, "کد معتبر نیست.")
        return render(request, self.template_name, {'form': form})

from django.contrib.auth.mixins import LoginRequiredMixin

class SignupView(View):
    template_name = "account/signup.html"
    form_class = SignupForm

    def get(self, request):
        phone = request.session.get('verified_phone')
        if not phone:
            messages.error(request, "ابتدا شماره را تایید کنید.")
            return redirect('account:send_otp')
        form = self.form_class(initial={'phone': phone})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            full_name = form.cleaned_data['full_name']
            role = form.cleaned_data['role']
            password = User.objects.make_random_password()
            user = User.objects.create_user(phone=phone, password=password, full_name=full_name)
            # اگر فروشنده است، seller_profile از قبل ساخته شده؛ می‌تواند اطلاعات را ویرایش کند
            auth.login(request, user)
            messages.success(request, "ثبت‌نام با موفقیت انجام شد.")
            return redirect('account:profile')
        return render(request, self.template_name, {'form': form})

class SigninView(View):
    template_name = "account/signin.html"
    form_class = SigninForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # در این پیاده‌سازی ورود با OTP پیشنهاد می‌شود؛ اینجا فقط ارسال OTP برای شماره داده‌شده ذخیره می‌شود
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            request.session['otp_phone'] = phone
            return redirect('account:send_otp')
        return render(request, self.template_name, {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    """نمایش پروفایل کاربر (ساده)"""
    return render(request, 'account/profile.html', {'user': request.user})

def signout_view(request):
    auth.logout(request)
    return redirect('product:product_list')