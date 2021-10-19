import mimetypes

from eCommerce.settings.base import *

DEBUG = True

mimetypes.add_type("application/javascript", ".js", True)
INTERNAL_IPS = ('127.0.0.1',)
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
