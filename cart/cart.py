from catalog.models import Product
from decimal import Decimal
from django.conf import settings


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price_current)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
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
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            yield product
        # for item in cart.values():
        #     item['price'] = item['price']
        #     item['total_price'] = str(Decimal(item['price']) * int(item['quantity']))
        #     yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def update(self):
        product_ids = self.cart.keys()
        pk_to_remove = []
        for pk in product_ids:
            try:
                product = Product.objects.get(pk=pk)
                self.cart[pk]['price'] = str(product.price_current)
                self.save()
            except:
                pk_to_remove.append(pk)
        for pk in pk_to_remove:
            self.remove(False, pk)

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()