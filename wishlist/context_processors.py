from .wishlist import Wishlist


def wishlist_processor(request):
    wishlist = Wishlist(request)
    wishlist.update()
    return {'wishlist': wishlist}
