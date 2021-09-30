from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .utils import get_filters, get_prices, get_filtered_products, get_filtered_products_p
import json


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

    query_filters = []
    if request.method == 'GET':
        filters = get_filters(request, category)
        prices = get_prices(products, request)
        for key in request.GET:
            query_filters.append({
                'key': key,
                'values': request.GET.getlist(key)
            })
        if len(query_filters):
            products = get_filtered_products(request, products, query_filters)

        context = {
            'category': category,
            'products': products,
            'filters': filters,
            'prices': prices,
        }
        return render(request, 'catalog/catalog.html', context)

    if request.method == 'POST':
        query_filters = json.loads(request.body)
        if len(query_filters):
            products = get_filtered_products_p(request, products, query_filters)

        context = {
            'products': products,
        }
        return render(request, 'catalog/products-list.html', context)


