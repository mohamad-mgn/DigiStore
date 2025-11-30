from django.db import transaction
from apps.user.models import User, CustomerProfile, SellerProfile

class UserService:

    @staticmethod
    @transaction.atomic
    def create_user(phone: str, full_name: str, role: str) -> User:
        user = User.objects.create(
            phone=phone,
            full_name=full_name,
            is_seller=(role == "seller")
        )
        if role == "customer":
            CustomerProfile.objects.create(user=user)
        else:
            SellerProfile.objects.create(user=user, store_name="فروشگاه جدید")
        return user