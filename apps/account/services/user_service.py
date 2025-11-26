from django.db import transaction
from apps.user.models import User, CustomerProfile, SellerProfile

class UserService:
    """
    UserService provides utilities for creating users along with
    their associated profiles (customer or seller) in a transactional way.
    """

    @staticmethod
    @transaction.atomic
    def create_user(phone: str, full_name: str, role: str) -> User:
        """
        Create a new user with the given phone, full name, and role.
        Automatically creates the corresponding profile (CustomerProfile or SellerProfile).

        Args:
            phone (str): The user's phone number.
            full_name (str): The user's full name.
            role (str): Either "customer" or "seller".

        Returns:
            User: The newly created User instance.
        
        Notes:
            - This method is wrapped in an atomic transaction to ensure
              that both the user and profile are created together.
            - SellerProfile defaults to a store name of "فروشگاه جدید".
        """
        # Create the user instance with role-based flag
        user = User.objects.create(
            phone=phone,
            full_name=full_name,
            is_seller=(role == "seller")
        )

        # Create the associated profile depending on the role
        if role == "customer":
            CustomerProfile.objects.create(user=user)
        else:
            SellerProfile.objects.create(user=user, store_name="فروشگاه جدید")

        return user