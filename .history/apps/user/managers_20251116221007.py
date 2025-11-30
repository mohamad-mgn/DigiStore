from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    UserManager سفارشی برای ایجاد کاربر با شماره موبایل به عنوان شناسه.
    """

    def create_user(self, phone, password=None, **extra_fields):
        """
        ساختن یک کاربر عادی.
        phone: شماره موبایل (الزامی)
        password: اختیاری — اگر داده نشود، رمز غیرقابل استفاده ست می‌شود.
        extra_fields: فیلدهای اضافی مثل full_name, is_seller, ...
        """
        if not phone:
            raise ValueError("کاربر باید شماره موبایل داشته باشد.")
        phone = str(phone).strip()
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        ساختن سوپر یوزر — رمز اجباری است.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if password is None:
            raise ValueError("ادمین باید رمز عبور داشته باشد.")
        return self.create_user(phone, password, **extra_fields)