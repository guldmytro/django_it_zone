from catalog.models import Product
from django.conf import settings


class Wishlist:
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.wishlist = wishlist

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = {
                'name': product.name
            }
        self.save()

    def save(self):
        # it will save session in database
        self.session.modified = True

    def remove(self, product, pk=False):
        product_id = ''
        if product:
            product_id = str(product.id)
        else:
            product_id = pk
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.wishlist.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            yield product

    def update(self):
        product_ids = self.wishlist.keys()
        pk_to_remove = []
        for pk in product_ids:
            try:
                Product.objects.get(pk=pk)
            except:
                pk_to_remove.append(pk)
        for pk in pk_to_remove:
            self.remove(False, pk)

    def __len__(self):
        return len(self.wishlist)

    def clear(self):
        del self.session[settings.WISHLIST_SESSION_ID]
        self.save()