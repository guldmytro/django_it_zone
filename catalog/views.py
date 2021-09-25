from django.shortcuts import render, get_object_or_404
from .models import Product


def index(request):
    return render(request, 'catalog/index.html', {})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {
        'product': product
    }
    print('Images:')
    print(product.images.all())
    return render(request, 'catalog/single.html', context)