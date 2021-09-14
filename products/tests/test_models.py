import os
from decimal import Decimal
from pathlib import Path
from shutil import rmtree

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import TestCase
from django.utils.text import slugify

from products.models import Product
from eCommerce.settings import MEDIA_ROOT

image_path = os.path.join(Path(__file__).resolve().parent, 'test_image.png')


class ProductModelTest(TestCase):
    def setUp(self):
        self.image = SimpleUploadedFile(name='test_image.png',
                                        content=open(image_path, 'rb').read(),
                                        content_type='image/jpeg')
        super(ProductModelTest, self).setUp()

    def tearDown(self):
        """ Delete MEDIA_ROOT of test time """
        # Check MEDIA_ROOT is not the main one
        if r'\test_media_root' in MEDIA_ROOT:
            rmtree(MEDIA_ROOT)
        super(ProductModelTest, self).tearDown()

    def test_create_product_with_valid_data(self):
        product_data = {
            'title': 'test',
            'slug': 'test',
            'image': self.image,
            'price': Decimal('20.99'),
            'description': 'Long text for description',
            'is_featured': False,
            'is_active': True,
        }
        Product.objects.create(**product_data)

        created_product = Product.objects.filter(title=product_data['title'])

        self.assertTrue(created_product.exists())
        self.assertEqual(created_product.count(), 1)
        testing_product = created_product.first()
        self.assertEqual(testing_product.slug, product_data['slug'])
        self.assertEqual(testing_product.price, product_data['price'])
        self.assertEqual(testing_product.description,
                         product_data['description'])
        self.assertEqual(testing_product.is_featured,
                         product_data['is_featured'])
        self.assertEqual(testing_product.is_active, product_data['is_active'])
        self.assertIsNotNone(testing_product.image)

    def test_title_is_unique(self):
        title = 'Product title'
        product_data = {
            'image': self.image,
            'price': 20,
            'description': 'Long description',
        }
        Product.objects.create(title=title, **product_data)

        error_msg = 'UNIQUE constraint failed: products_product.title'
        with self.assertRaisesRegex(IntegrityError, error_msg):
            Product.objects.create(title=title, **product_data)

    def test_slug_is_creating_automatically(self):
        product_data = {
            'title': 'test',
            'image': self.image,
            'price': 20,
            'description': 'Long description',
        }
        product = Product.objects.create(**product_data)

        self.assertIsNotNone(product.slug)
        self.assertEqual(product.slug, slugify(product_data['title']))

    def test_slug_is_unique(self):
        slug = 'Product-slug'
        product_data = {
            'image': self.image,
            'price': 20,
            'description': 'Long description',
        }
        Product.objects.create(slug=slug, title='pro1', **product_data)

        error_msg = 'UNIQUE constraint failed: products_product.slug'
        with self.assertRaisesRegex(IntegrityError, error_msg):
            Product.objects.create(slug=slug, title='pro2', **product_data)
