from catalog.models import Product
from catalog.models import Attribute
from catalog.models import Kit
from .models import Brand
from unidecode import unidecode
from django.utils.text import slugify


def parse_brands():
    products = Product.objects.all()
    brand_attribute = Attribute.objects.get(slug='brend')
    for product in products:
        k = Kit.objects.get(product=product, attribute=brand_attribute)
        if k:
            b = Brand.objects.get_or_create(title=k.value, slug=slugify(unidecode(k.value)))
            product.brand = b[0]
            product.save()


def parse_letters():
    brands = Brand.objects.all()
    letters = []
    for brand in brands:
        letter = str(brand.title[0]).lower()
        if letter not in letters:
            letters.append(letter)
    return letters


def parse_url(query_str):
    params = query_str.split(';')
    result = {}
    for p in params:
        p_list = p.split(':')
        if len(p_list) == 2:
            result[p_list[0].lower()] = str(p_list[1].lower())
    return result
