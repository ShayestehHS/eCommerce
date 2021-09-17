from random import choice
from string import ascii_lowercase, digits


def random_string_generator(size=10, chars=ascii_lowercase + digits):
    return ''.join(choice(chars) for _ in range(size))


def unique_order_id_generator(instance, size):
    while True:
        new_order_id = random_string_generator(size)
        Klass = instance.__class__
        qs_exists = Klass.objects.filter(order_id=new_order_id).exists()
        if not qs_exists:
            return new_order_id.upper()
