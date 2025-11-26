from django.contrib.auth.base_user import BaseUserManager

# Custom user manager to handle users with phone numbers instead of username
class UserManager(BaseUserManager):

    # Method to create a regular user
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("کاربر باید شماره موبایل داشته باشد.")  # Raise error if phone is not provided
        phone = str(phone).strip()  # Clean up the phone number
        user = self.model(phone=phone, **extra_fields)  # Create user instance
        if password:
            user.set_password(password)  # Set hashed password
        else:
            user.set_unusable_password()  # If no password, set as unusable
        user.save(using=self._db)  # Save user in database
        return user

    # Method to create a superuser
    def create_superuser(self, phone, password, **extra_fields):
        # Set default fields for superuser
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if password is None:
            raise ValueError("ادمین باید رمز عبور داشته باشد.")  # Ensure superuser has a password
        return self.create_user(phone, password, **extra_fields)  # Call create_user with superuser fields