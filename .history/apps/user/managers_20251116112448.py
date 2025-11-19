from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    مدیر اختصاصی برای User سفارشی.
    شماره موبایل به جای username استفاده می‌شود.
    """

    def normalize_phone(self, phone: str) -> str:
        """نرمال‌سازی شماره موبایل به فرمت 09xxxxxxxxx"""
        phone = str(phone).strip().replace(" ", "").replace("-", "")

        if phone.startswith("+98"):
            phone = "0" + phone[3:]
        elif phone.startswith("98"):
            phone = "0" + phone[2:]

        return phone

    def create_user(self, phone, password=None, **extra_fields):
        """ساخت کاربر عادی"""
        if not phone:
            raise ValueError("کاربر باید شماره موبایل داشته باشد.")

        phone = self.normalize_phone(phone)

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(phone=phone, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """ساخت سوپریوزر"""
        if not password:
            raise ValueError("ادمین باید رمز عبور داشته باشد.")

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("سوپریوزر باید is_staff=True باشد.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("سوپریوزر باید is_superuser=True باشد.")

        return self.create_user(phone, password, **extra_fields)