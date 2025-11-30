from django.urls import path
from .views import SendOTPView, VerifyOTPView, SignupView, SigninView, profile_view, signout_view

app_name = 'account'

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('profile/', profile_view, name='profile'),
    path('signout/', signout_view, name='signout'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]