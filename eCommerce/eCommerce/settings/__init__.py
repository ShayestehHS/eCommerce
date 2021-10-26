setting_env = 'PRODUCTION'  # Choices are: LOCAL, PRODUCTION, TEST

if setting_env == 'LOCAL':
    from eCommerce.settings.local import *
    print("-- Local setting imported --")
elif setting_env == 'PRODUCTION':
    from eCommerce.settings.production import *
    print("-- Production setting imported --")
elif setting_env == "TEST":
    from eCommerce.settings.test import *
    print("-- Test setting imported --")
else:
    raise Exception('-- Invalid setting_env --')
