from django.db import models
from django.db.models.signals import pre_save, m2m_changed
from django.conf import settings
from django.dispatch import receiver

from products.models import Product

User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new(self, user=None):
        user = user if user and user.is_authenticated else None
        cart = self.model.objects.create(user=user)

        return cart

    def get_or_new(self, user=None, **kwargs):
        try:
            print(kwargs.get('id'))
            obj, is_new = self.model.objects.get(**kwargs), False
        except self.model.DoesNotExist:
            user = user if user.is_authenticated else None
            obj, is_new = self.model.objects.new(user=user), True

        return obj, is_new


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    products = models.ManyToManyField(Product,
                                      blank=True, null=True)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                   help_text='Maximum subtotal is 99999.99')
    total = models.DecimalField(max_digits=7, decimal_places=2, default=0,
                                help_text='Maximum total is 99999.99')
    last_update = models.DateTimeField(auto_now=True)
    crated = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return f"cart {self.id}"


@receiver(m2m_changed, sender=Cart.products.through)
def m2m_changed_receiver(sender, instance, action, **kwargs):
    if 'post_' in action:  # post_save post_remove post_clear
        subtotal = 0
        for product in instance.products.all():
            subtotal += product.price

        instance.subtotal = subtotal
        instance.total = subtotal  # *1.08
        instance.save(update_fields=['subtotal', 'total'])
