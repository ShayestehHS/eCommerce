from django.db import models
from django.conf import settings
from django.urls import reverse

from address.models import Address
from carts.models import Cart
from eCommerce.utils import update_session

User = settings.AUTH_USER_MODEL

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('shipped', 'Shipped'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
)


class OrderQuerySet(models.query.QuerySet):
    def not_created(self):
        return self.exclude(status='created')


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def not_created(self):
        return self.get_queryset().not_created()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(to=Cart, on_delete=models.CASCADE, related_name='order')
    order_id = models.CharField(max_length=10, editable=False, blank=True)
    address_shipping = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_shipping', null=True, blank=True)
    address_billing = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_billing', null=True, blank=True)
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=8, default='created')
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0, help_text='Maximum subtotal is 99999.99')
    timestamp = models.DateField(auto_now=True)

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp']

    def check_done(self):
        if self.cart.is_all_digital:
            address_shipping = True  # Because is not required anymore
        else:
            address_shipping = self.address_shipping_id

        if address_shipping and self.address_billing_id:
            return True
        return False

    def deactivate_cart(self, request, checked=False):
        done = True if checked else self.check_done()
        if not done:
            return False

        cart = self.cart

        self.status = 'paid'
        self.save(update_fields=['status', 'total'])

        cart.is_active = False
        cart.save(update_fields=['is_active'])

        new_cart = Cart.objects.new(request)

        update_session(request, new_cart, is_new=True)

        return True

    def __str__(self):
        return self.order_id

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={'pk': self.pk})
