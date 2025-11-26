from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.account.services.otp_service import OTPService
from apps.user.models import User
from .forms import (
    SendOTPForm, VerifyOTPForm, SignupForm,
    SigninForm, EditCustomerProfileForm, EditSellerProfileForm
)

# -----------------------------
# Send OTP View
# -----------------------------
class SendOTPView(View):
    """
    Handle sending OTP to a user's phone.
    GET: Display phone input form.
    POST: Validate phone and send OTP.
    """
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


# -----------------------------
# Verify OTP View
# -----------------------------
class VerifyOTPView(View):
    """
    Handle OTP verification.
    GET: Display verification form.
    POST: Validate OTP, login user or redirect to signup.
    """
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


# -----------------------------
# Signup View
# -----------------------------
class SignupView(View):
    """
    Handle new user registration.
    GET: Display signup form.
    POST: Create user based on role and log in.
    """
    template_name = "account/signup.html"

    def get(self, request, phone):
        form = SignupForm(initial={"phone": phone})
        return render(request, self.template_name, {"form": form, "phone": phone})

    def post(self, request, phone):
        form = SignupForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            role = form.cleaned_data["role"]

            # Create user with role-based flag
            user = User.objects.create(
                phone=phone,
                full_name=full_name,
                is_seller=(role == "seller"),
            )

            # Log the user in
            login(request, user)
            return redirect("home:index")

        return render(request, self.template_name, {"form": form, "phone": phone})


# -----------------------------
# Signin View
# -----------------------------
class SigninView(View):
    """
    Handle user login by phone.
    GET: Display login form.
    POST: Validate phone and send OTP.
    """
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


# -----------------------------
# Signout View
# -----------------------------
class SignoutView(View):
    """
    Handle user logout.
    """
    def get(self, request):
        logout(request)
        return redirect("account:signin")


# -----------------------------
# Profile View
# -----------------------------
class ProfileView(LoginRequiredMixin, View):
    """
    Display the user's profile.
    """
    template_name = "account/profile_view.html"

    def get(self, request):
        user = request.user
        profile = user.seller_profile if user.is_seller else user.customer_profile
        return render(request, self.template_name, {
            "user": user,
            "profile": profile
        })


# -----------------------------
# Profile Edit View
# -----------------------------
class ProfileEditView(LoginRequiredMixin, View):
    """
    Handle editing of user profiles.
    Selects the form and template based on user role.
    """

    def get_form_and_template(self, user):
        """
        Determine the form class, template, and profile instance
        based on whether the user is a seller or customer.
        """
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
            # Save profile and update user's full name
            form.save(user=request.user)
            messages.success(request, "پروفایل ذخیره شد.")
            return redirect("account:profile")
        return render(request, template, {"form": form})