import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

from accounts.utils import create_email_code
from eCommerce.utils import custom_send_email


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
        user.is_registered = True
        user.is_staff = True
        user.full_name = "Admin"
        user.save(using=self._db, update_fields=['is_superuser', 'is_staff', 'is_registered', 'full_name'])

        return user


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(max_length=127, unique=True)
    full_name = models.CharField(max_length=127)
    unique_code = models.CharField(null=True, blank=True, max_length=16)
    confirm_code = models.PositiveIntegerField(null=True, blank=True)
    chance_to_try = models.PositiveSmallIntegerField(default=3)
    is_registered = models.BooleanField(default=False)
    # ToDo: Activation can expire after some days.

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def send_activation_email(self):
        self.is_registered = False
        self.confirm_code = create_email_code(6)
        self.unique_code = uuid.uuid4().hex[:16].upper()
        self.save(update_fields=['is_registered', 'confirm_code', 'unique_code'])

        custom_send_email(title="Email confirmation", to=[self.email],
                          context={'unique_code': self.confirm_code},
                          template_name='email/confirm_code.html')

    def fail_activation(self):
        try:
            self.delete()
        except:
            self.is_active = False
            self.save(update_fields=['is_active'])
            # ToDo: Log this situation

    def register(self):
        self.is_registered = True
        self.save(update_fields=['chance_to_try', 'is_registered'])

    def __str__(self):
        return self.email


class ContactEmail(models.Model):  # Contact to us
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=127)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
