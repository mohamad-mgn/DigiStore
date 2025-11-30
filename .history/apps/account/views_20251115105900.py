from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages, auth
from django.utils import timezone
from django.conf import settings
from .forms import SendOTPForm, VerifyOTPForm, SignupForm, SigninForm
from .models import MobileOTP
from apps.user.models import User
from .services.sms import sms_service
from datetime import timedelta
import random

# تنظیمات قابل تغییر:
OTP_LENGTH = 6
OTP_TTL_MINUTES = 5
OTP_RESEND_SECONDS = 60   # کاربر چند ثانیه باید منتظر بماند تا resend کند
OTP_MAX_PER_HOUR = 5      # حداکثر ارسال کد در یک ساعت برای یک شماره
OTP_MAX_ATTEMPTS = 5      # حداکثر تلاش برای حدس کد

def generate_otp():
    return f"{random.randint(10**(OTP_LENGTH-1), 10**OTP_LENGTH - 1)}"

def _can_send_more(phone: str) -> bool:
    """
    بررسی تعداد OTPهای ارسال شده در یک ساعت گذشته
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    sent_count = MobileOTP.objects.filter(phone=phone, created_at__gte=one_hour_ago).count()
    return sent_count < OTP_MAX_PER_HOUR

def _seconds_until_resend(phone: str) -> int:
    latest = MobileOTP.objects.filter(phone=phone).order_by('-created_at').first()
    if not latest:
        return 0
    delta = timezone.now() - latest.created_at
    remaining = OTP_RESEND_SECONDS - int(delta.total_seconds())
    return max(0, remaining)

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
            # چک resend
            wait = _seconds_until_resend(phone)
            if wait > 0:
                messages.error(request, f"لطفاً {wait} ثانیه صبر کنید تا دوباره کد ارسال شود.")
                return redirect('account:send_otp')

            if not _can_send_more(phone):
                messages.error(request, "حداکثر دفعات ارسال کد در ساعت برای این شماره انجام شده است. بعداً تلاش کنید.")
                return redirect('account:send_otp')

            code = generate_otp()
            # ذخیره کد
            MobileOTP.objects.create(phone=phone, code=code)
            # ارسال با سرویس sms (mock یا واقعی)
            sms_service.send_code(phone, code)
            # نگهداری شماره در session برای استفاده در verify/signup
            request.session['otp_phone'] = phone
            messages.success(request, "کد تایید برای شماره شما ارسال شد.")
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
            otp = MobileOTP.objects.filter(phone=phone, verified=False).order_by('-created_at').first()
            if not otp:
                messages.error(request, "برای این شماره کدی ارسال نشده است یا منقضی شده است.")
                return redirect('account:send_otp')

            # بررسی منقضی شدن
            if otp.is_expired():
                messages.error(request, "کد منقضی شده است. دوباره ارسال کنید.")
                return redirect('account:send_otp')

            # محافظت نسبت به تلاش‌های زیاد
            if otp.attempts >= OTP_MAX_ATTEMPTS:
                messages.error(request, "تعداد تلاش‌های شما برای وارد کردن کد بیش از حد مجاز بوده است.")
                return redirect('account:send_otp')

            if otp.code == code:
                otp.mark_verified()
                # اگر کاربر موجود است -> لاگین، وگرنه به صفحه ثبت‌نام برو
                try:
                    user = User.objects.get(phone=phone)
                    auth.login(request, user)
                    messages.success(request, "ورود با موفقیت انجام شد.")
                    return redirect('product:product_list')
                except User.DoesNotExist:
                    # برو به صفحه ثبت‌نام و به آنجا phone را پاس بده
                    request.session['verified_phone'] = phone
                    return redirect('account:signup')
            else:
                otp.increment_attempts()
                messages.error(request, "کد وارد شده صحیح نیست.")
        return render(request, self.template_name, {'form': form})

class SignupView(View):
    template_name = "account/signup.html"
    form_class = SignupForm

    def get(self, request):
        phone = request.session.get('verified_phone') or request.session.get('otp_phone')
        if not phone:
            messages.error(request, "ابتدا شماره خود را تایید کنید.")
            return redirect('account:send_otp')
        form = self.form_class(initial={'phone': phone})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            full_name = form.cleaned_data.get('full_name') or ''
            role = form.cleaned_data.get('role') or 'customer'
            # اگر کاربری از قبل وجود دارد، جلوی duplicate بگیر
            user, created = User.objects.get_or_create(phone=phone, defaults={'full_name': full_name})
            if created:
                # رمز را به صورت رندوم بساز و ذخیره کن، کاربر عموماً با OTP وارد خواهد شد
                user.set_unusable_password()
                user.save()
            # تنظیم نقش: اگر seller انتخاب شد، seller_profile در سیگنال اولیه وجود دارد — بعداً تکمیلش می‌کند
            auth.login(request, user)
            messages.success(request, "ثبت‌نام و ورود با موفقیت انجام شد.")
            return redirect('product:product_list')
        return render(request, self.template_name, {'form': form})

class SigninView(View):
    template_name = "account/signin.html"
    form_class = SigninForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            # شروع فرایند ارسال OTP
            request.session['otp_phone'] = phone
            return redirect('account:send_otp')
        return render(request, self.template_name, {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # صفحهٔ پروفایل ساده که بعداً گسترش خواهیم داد
    return render(request, 'account/profile.html', {'user': request.user})

def signout_view(request):
    auth.logout(request)
    return redirect('product:product_list')