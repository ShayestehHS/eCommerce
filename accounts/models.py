from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if email is None:
            raise ValueError("User must have 'email'")
        if password is None:
            raise ValueError("User must have 'password'")

        user = self.model.objects.create(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email, password, **kwargs)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db, update_fields=['is_superuser', 'is_staff'])

        return user


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(max_length=127, unique=True)
    full_name = models.CharField(max_length=127)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
