from .cart import Cart
from .forms import CartAddProductForm


def cart_processor(request):
    cart = Cart(request)
    cart.update()
    return {'cart_len': len(cart)}


def add_to_cart_processor(request):
    cart_product_form = CartAddProductForm()
    return {'cart_product_form': cart_product_form}
