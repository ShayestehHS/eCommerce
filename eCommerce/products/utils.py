from products.models import Product


def validate_id(product_id):
    if product_id is None:
        raise ValueError('Product id is "None"')

    try:
        product_id = int(product_id)
        return product_id
    except ValueError:
        raise ValueError('Product id is not Integer')


def get_product(product_id, is_valid=False):
    """ Get product with validated product_id """
    product_id = product_id if is_valid else validate_id(product_id)

    try:
        obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise ValueError(f'Product with id {product_id} is not exists')

    return obj
