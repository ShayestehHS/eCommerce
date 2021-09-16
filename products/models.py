import os
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.text import slugify

from taggit.managers import TaggableManager


def get_image_upload_path(instance, filename):
    return os.path.join('Products', 'images', instance.title, filename)


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(is_featured=True)

    def active(self):
        return self.filter(is_active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(tags__name__icontains=query))
        return self.filter(lookups, is_active=True).distinct()


class ProductModelManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, self._db)

    def featured(self):
        return self.get_queryset().featured()

    def active(self):
        return self.get_queryset().active()

    def search(self, query):
        return self.get_queryset().search(query)


class Product(models.Model):
    title = models.CharField(max_length=120, unique=True,
                             help_text="Maximum length is 120 character.")
    slug = models.SlugField(blank=True, unique=True,
                            help_text="This field is not required.")
    image = models.ImageField(upload_to=get_image_upload_path)
    price = models.DecimalField(max_digits=5, decimal_places=2,
                                help_text="Maximum price is 999.99")
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)

    objects = ProductModelManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})
