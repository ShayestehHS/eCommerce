import os
from django.db import models
from django.db.models import Q
from django.urls import reverse

from taggit.managers import TaggableManager


def get_image_upload_path(instance, filename):
    return os.path.join('Products', 'images', instance.name, filename)


class ProductQuerySet(models.query.QuerySet):
    def all_id(self):
        return self.all().values_list('id', flat=True)

    def featured(self):
        return self.filter(is_featured=True)

    def active(self):
        return self.filter(is_active=True)

    def search(self, query, *args):
        lookups = (Q(name__icontains=query) |
                   Q(description__icontains=query) |
                   Q(tags__name__icontains=query))
        return self.filter(lookups, is_active=True).distinct()


class ProductModelManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, self._db)

    def all_id(self):
        return self.get_queryset().all_id()

    def featured(self):
        return self.get_queryset().featured()

    def active(self):
        return self.get_queryset().active()

    def search(self, query, *args):
        return self.get_queryset().search(query, *args)


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True, help_text="Maximum length is 120 character.")
    slug = models.SlugField(blank=True, unique=True, max_length=130, help_text="This field is not required.")
    image = models.ImageField(upload_to=get_image_upload_path)
    price = models.DecimalField(max_digits=5, decimal_places=2, help_text="Maximum price is 999.99")
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)

    objects = ProductModelManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})
