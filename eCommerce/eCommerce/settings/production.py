from eCommerce.settings.base import *

DEBUG = bool(int(os.getenv("DEBUG", default=0)))
# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.getenv("DJANGO_ALLOWED_HOSTS", default="*").split(" ")
    )
)
SECRET_KEY = os.getenv('SECRET_KEY')

DOMAIN_NAME = 'shayestehhs.ir'

STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'

STATIC_ROOT = '/vol/web/static'
MEDIA_ROOT = '/vol/web/media'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'PORT': '5432',
    }
}

# SSL/TLS Settings
# CORS_REPLACE_HTTPS_REFERER = True
# HOST_SCHEME = "https://"
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS = 1000000
# SECURE_FRAME_DENY = True

MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = os.getenv('MAILCHIMP_DATA_CENTER')
MAILCHIMP_PUB_KEY = os.getenv('MAILCHIMP_PUB_KEY')

MERCHANT = os.getenv('MERCHANT')

# Celery configuration
BROKER_URL = f'redis://{DOMAIN_NAME}:6379'
CELERY_RESULT_BACKEND = f'redis://{DOMAIN_NAME}:6379'
