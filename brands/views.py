from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .utils import parse_brands, parse_letters, parse_url
from .models import Brand
from catalog.models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from shop.settings import TITLE_SUFFIX


def index(request):
    # parse_brands()
    letters = parse_letters()
    breadcrumbs = [{
                'label': 'Поставщики',
                'url': '',
                'type': 'text'
            }]
    brands = Brand.objects.all()
    paginator = Paginator(brands, 10)
    page = 1
    try:
        brands = paginator.page(page)
    except PageNotAnInteger:
        brands = paginator.page(1)
    except EmptyPage:
        brands = paginator.page(paginator.num_pages)

    title = f'Поставщики{TITLE_SUFFIX}'
    context = {
        'letters': letters,
        'brands': brands,
        'breadcrumbs': breadcrumbs,
        'title': title
    }
    return render(request, 'brands/archive.html', context)


def filter(request, str):
    filters = parse_url(str)
    brands = Brand.objects.all()
    letters = parse_letters()
    breadcrumbs = [{
        'label': 'Поставщики',
        'url': '',
        'type': 'text'
    }]
    if 'letter' in filters:
        brands = brands.filter(title__istartswith=filters['letter'])
    if 'filter' in filters and filters['filter'] == 'top':
        brands = brands.filter(top=True)

    paginator = Paginator(brands, 10)
    page = 1
    if 'page' in filters:
        page = int(filters['page'])
    try:
        brands = paginator.page(page)
    except PageNotAnInteger:
        brands = paginator.page(1)
    except EmptyPage:
        brands = paginator.page(paginator.num_pages)

    title = f'Поставщики{TITLE_SUFFIX}'
    context = {
        'letters': letters,
        'brands': brands,
        'breadcrumbs': breadcrumbs,
        'title': title
    }
    return render(request, 'brands/archive.html', context)


def detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    breadcrumbs = [{
            'label': 'Поставщики',
            'url': reverse('brands:home'),
            'type': 'link'
        },
        {
            'label': brand.title,
            'url': '',
            'type': 'text'
        }]
    title = f'{brand.title}{TITLE_SUFFIX}'
    products = Product.objects.filter(brand=brand)
    paginator = Paginator(products, 12)
    page = 1
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'products': products,
        'brand': brand,
        'breadcrumbs': breadcrumbs,
        'title': title
    }
    return render(request, 'brands/detail.html', context)


def detail_paged(request, slug, paged):
    brand = get_object_or_404(Brand, slug=slug)
    breadcrumbs = [{
            'label': 'Поставщики',
            'url': reverse('brands:home'),
            'type': 'link'
        },
        {
            'label': brand.title,
            'url': '',
            'type': 'text'
        }]
    products = Product.objects.filter(brand=brand)
    paginator = Paginator(products, 12)
    page = paged
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'products': products,
        'brand': brand,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'brands/detail.html', context)
