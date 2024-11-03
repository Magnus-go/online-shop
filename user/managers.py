from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, fullname, phone_number, password):
        if not email:
            raise ValueError('User most have email')

        user = self.model(
            email=self.normalize_email(email),
            fullname=fullname,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, fullname, phone_number):
        user = self.create_user(
            email,
            fullname,
            phone_number,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)
        return user
