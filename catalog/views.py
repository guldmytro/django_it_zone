from django.shortcuts import render, get_object_or_404
from .models import Product


def index(request):
    return render(request, 'catalog/index.html', {})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_attributes = []
    for attribute in product.attributes.all():
        kit = attribute.kit_set.get(product=product)
        product_attributes.append({
            'name': attribute.name,
            'value': kit.value
        })
    context = {
        'product': product,
        'product_attributes': product_attributes
    }
    return render(request, 'catalog/single.html', context)