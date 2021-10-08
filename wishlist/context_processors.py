from .wishlist import Wishlist


def wishlist_processor(request):
    wishlist = Wishlist(request)
    return {'wishlist': wishlist}
