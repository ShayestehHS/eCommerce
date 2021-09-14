import os
from django.db import models
from django.utils.text import slugify


def get_image_upload_path(instance, filename):
    return os.path.join('Products', 'images', instance.title, filename)


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        self.filter(is_featured=True)

    def active(self):
        self.filter(is_active=True)


class ProductModelManager(models.Manager):
    def featured(self):
        self.get_queryset().filter(is_featured=True)

    def active(self):
        self.get_queryset().filter(is_active=True)


class Product(models.Model):
    title = models.CharField(max_length=120,
                             help_text="Maximum length is 120 character.")
    slug = models.SlugField(blank=True, unique=True,
                            help_text="This field is not required.")
    image = models.ImageField(upload_to=get_image_upload_path, )
    price = models.DecimalField(max_digits=5, decimal_places=2,
                                help_text="Maximum price is 999.99")
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = ProductModelManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
