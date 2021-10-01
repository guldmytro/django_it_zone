from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .utils import get_filters, get_prices, get_filtered_products, get_filtered_products_p, get_page_from_query, \
    get_full_path_from_query
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q


def index(request):
    return render(request, 'catalog/index.html', {})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    category = product.category
    parent_category = category.parent_category
    product_attributes = []
    breadcrumbs = []
    breadcrumbs.append({
        'label': parent_category.name,
        'url': parent_category.get_absolute_url,
        'type': 'link'
    })
    breadcrumbs.append({
        'label': category.name,
        'url': category.get_absolute_url,
        'type': 'link'
    })

    breadcrumbs.append({
        'label': product.name,
        'url': product.get_absolute_url,
        'type': 'text'
    })

    for attribute in product.attributes.all():
        kit = attribute.kit_set.get(product=product)
        product_attributes.append({
            'name': attribute.name,
            'value': kit.value
        })
    context = {
        'product': product,
        'product_attributes': product_attributes,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'catalog/single.html', context)


def products_by_cat(request, slug):
    category = get_object_or_404(Category, slug=slug)
    children_categories = category.category_set.all()
    q = Q(category=category)
    for children_category in children_categories:
        q |= Q(category=children_category)

    products_list = Product.objects.filter(q)

    form = SearchForm()
    query = None
    if 'query' in request.GET:
        prices = get_prices(products_list, request)
        filters = get_filters(request, category, children_categories)
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            products_list = products_list.annotate(similarity=TrigramSimilarity('name', query))\
                .filter(similarity__gt=0.045).order_by('-similarity')

            context = {
                'category': category,
                'products': products_list,
                'prices': prices,
                'filters': filters,
                'search_form': form,
                'query_string': query,
            }

            return render(request, 'catalog/catalog.html', context)

    query_filters = []
    if request.method == 'GET':
        filters = get_filters(request, category, children_categories)
        prices = get_prices(products_list, request)
        for key in request.GET:
            query_filters.append({
                'key': key,
                'values': request.GET.getlist(key)
            })
        if len(query_filters):
            try:
                products_list = get_filtered_products(request, products_list, query_filters)
            except:
                products_list = []

        paginator = Paginator(products_list, 12)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        full_path = ''
        try:
            full_path = request.get_full_path().split('?')[1]
            full_path = full_path.replace('page', 'non-page')
        except:
            pass

        breadcrumbs = []
        parent_category = category.parent_category
        if parent_category:
            breadcrumbs.append({
                'label': parent_category.name,
                'url': parent_category.get_absolute_url,
                'type': 'link'
            })
        breadcrumbs.append({
            'label': category.name,
            'url': category.get_absolute_url,
            'type': 'text'
        })
        context = {
            'category': category,
            'products': products,
            'filters': filters,
            'prices': prices,
            'full_path': full_path,
            'search_form': form,
            'breadcrumbs': breadcrumbs
        }
        return render(request, 'catalog/catalog.html', context)

    if request.method == 'POST':
        query_filters = json.loads(request.body)
        if len(query_filters):
            try:
                products_list = get_filtered_products_p(request, products_list, query_filters)
            except:
                products_list = []

        paginator = Paginator(products_list, 12)
        page = get_page_from_query(query_filters)
        full_path = get_full_path_from_query(query_filters)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context = {
            'products': products,
            'full_path': full_path
        }
        return render(request, 'catalog/products-list.html', context)


