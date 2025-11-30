# apps/account/services/user_service.py

from apps.user.models import User, CustomerProfile, SellerProfile


class UserService:

    @staticmethod
    def create_user(phone: str, full_name: str, role: str) -> User:
        """
        ساخت کاربر بعد از تایید OTP
        """
        user = User.objects.create(
            phone=phone,
            full_name=full_name,
            is_seller=(role == "seller")
        )

        # ساخت پروفایل مناسب
        if role == "customer":
            CustomerProfile.objects.create(user=user)
        else:
            SellerProfile.objects.create(user=user, store_name="فروشگاه جدید")

        return user