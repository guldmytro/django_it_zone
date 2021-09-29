from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .utils import get_filters


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


def products_by_cat(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    filters = get_filters(category)
    context = {
        'category': category,
        'products': products,
        'filters': filters
    }
    return render(request, 'catalog/catalog.html', context)
