from django.urls import path
from .views import (
    send_otp_view,
    verify_otp_view,
    signup_view,
    signin_view,
    signout_view,
    profile_view,
    profile_edit_view,
)

app_name = 'account'

urlpatterns = [

    # 🔹 مرحله ۱: ارسال OTP
    path('send-otp/', send_otp_view, name='send_otp'),

    # 🔹 مرحله ۲: تأیید OTP
    path('verify/<str:phone>/', verify_otp_view, name='verify_otp'),

    # 🔹 مرحله ۳: ثبت‌نام بعد از تأیید OTP
    path('signup/<str:phone>/', signup_view, name='signup'),

    # 🔹 ورود و خروج
    path('signin/', signin_view, name='signin'),
    path('signout/', signout_view, name='signout'),

    # 🔹 پروفایل
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),

]