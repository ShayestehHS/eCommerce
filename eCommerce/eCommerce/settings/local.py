import mimetypes

from eCommerce.settings.base import *

DEBUG = True

SECRET_KEY = 'django-insecure-&i)&qam9h@lhpfa1mc_a@jay_zu3xq9v$w&)&1tb)89%m2)%t7'
mimetypes.add_type("application/javascript", ".js", True)
INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


# SSL/TLS Settings
# Set as default
CORS_REPLACE_HTTPS_REFERER = False
HOST_SCHEME = "http://"
SECURE_PROXY_SSL_HEADER = None
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = None
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_FRAME_DENY = False