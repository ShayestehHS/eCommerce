setting_env = 'PRODUCTION'  # Choices are: LOCAL, PRODUCTION, TEST
# Colors
ENDC = '\033[0m'
WARNING = '\033[93m'
OKGREEN = '\033[92m'
OKCYAN = '\033[96m'

if setting_env == 'LOCAL':
    from eCommerce.settings.local import *
    print(OKCYAN + "-- Local setting imported --" + ENDC)

elif setting_env == 'PRODUCTION':
    from eCommerce.settings.production import *
    print(OKCYAN + "-- Production setting imported --" + ENDC)

elif setting_env == "TEST":
    from eCommerce.settings.test import *
    print(OKCYAN + "-- Test setting imported --" + ENDC)

else:
    raise Exception(OKCYAN + '-- Invalid setting_env --' + ENDC)

if DEBUG is True:
    print(WARNING + "-- Debug mode is: ON --" + ENDC)
else:
    print(OKGREEN + "-- Debug mode is: OFF --" + ENDC)
