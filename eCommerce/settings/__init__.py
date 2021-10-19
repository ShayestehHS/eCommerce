setting_env = 'LOCAL'  # Choices are: LOCAL, PRODUCTION, TEST

if setting_env == 'LOCAL':
    from eCommerce.settings.local import *
elif setting_env == 'PRODUCTION':
    from eCommerce.settings.production import *
elif setting_env == "TEST":
    from eCommerce.settings.test import *
else:
    raise Exception('Invalid setting_env')
