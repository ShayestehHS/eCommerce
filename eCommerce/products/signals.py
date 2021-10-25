from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from products.models import Product


@receiver(post_save, sender=Product)
def product_post_save(instance, created, *args, **kwargs):
    is_name_updated = slugify(instance.name) != instance.slug

    if created or is_name_updated:
        instance.slug = slugify(instance.name)
        instance.save(update_fields=['slug'])

# ToDo: If product is_featured => Send message to subscribers by using pre_save signal
