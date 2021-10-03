from .cart import Cart


def cart_processor(request):
    cart = Cart(request)
    return {'cart_len': len(cart)}
