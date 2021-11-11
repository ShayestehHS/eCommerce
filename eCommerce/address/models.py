from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

TYPE_CHOICES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)

# ToDo: Change the model. address_1, address_2
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    address_type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    address_1 = models.CharField(max_length=127)
    address_2 = models.CharField(max_length=127, blank=True, null=True)
    country = models.CharField(max_length=63)
    city = models.CharField(max_length=63)
    state = models.CharField(max_length=63)
    postal_code = models.PositiveIntegerField()
    phone_number = models.PositiveIntegerField()

    def __str__(self):
        return self.address_1[0:20]
