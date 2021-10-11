from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Category, Delivery
from .utils import get_filters, get_prices, get_filtered_products, get_filtered_products_p, get_page_from_query, \
    get_full_path_from_query
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from reviews.forms import ReviewForm
from random import shuffle
from blog.models import Article
from config.models import Config
from django.core.mail import EmailMessage
from contacts.models import Contact


def index(request):
    articles = Article.published.all()[:12]
    top_products = Product.objects.all().order_by('-sales')[:4]
    exclude_list = list(item.id for item in top_products)
    new_products = Product.objects.exclude(pk__in=exclude_list)[:4]
    new_products_r = list(new_products)
    shuffle(new_products_r)
    config = Config.objects.first()
    banner_products = list(config.main_product.all())
    shuffle(banner_products)
    brands = config.brands.all()
    context = {
        'top_products': top_products,
        'articles': articles,
        'new_products': new_products_r,
        'banner_product': banner_products[0],
        'brands': brands
    }
    return render(request, 'catalog/index.html', context)


def product_detail(request, slug):
    delivery = Delivery.objects.first()
    product = get_object_or_404(Product, slug=slug)
    review_form = ReviewForm(initial={'product': product,
                                      'rating': 5})
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save()
            if request.is_ajax:
                return render(request, 'reviews/review-detail.html', {'review': review})

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
    similar_products = list(Product.objects.filter(category=category).exclude(id=product.id))
    shuffle(similar_products)
    accessories_cats = product.accessories.all()
    accessories = list(Product.objects.filter(category__in=accessories_cats))
    shuffle(accessories)
    context = {
        'product': product,
        'product_attributes': product_attributes,
        'breadcrumbs': breadcrumbs,
        'review_form': review_form,
        'similar_products': similar_products[:24],
        'accessories': accessories,
        'delivery': delivery
    }
    return render(request, 'catalog/single.html', context)


def products_by_cat(request, slug):
    category = get_object_or_404(Category, slug=slug)
    children_categories = category.category_set.all()
    q = Q(category=category)
    for children_category in children_categories:
        q |= Q(category=children_category)

    products_list = Product.objects.filter(q).order_by('-sales')

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
                'products': products_list,
                'prices': prices,
                'filters': filters,
                'search_form': form,
                'query_string': query,
                'breadcrumbs': breadcrumbs
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


def search(request):
    if 'query' in request.GET:
        products_list = Product.objects.all()
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            products_list = products_list.annotate(similarity=TrigramSimilarity('name', query))\
                .filter(similarity__gt=0.045).order_by('-similarity')
            breadcrumbs = [{
                'label': f'Результаты поиска "{query}"',
                'url': '',
                'type': 'text'
            }]
            context = {
                'products': products_list,
                'query_string': query,
                'breadcrumbs': breadcrumbs
            }
            return render(request, 'catalog/search.html', context)
    return redirect('catalog:home')


def question(request):
    page = Contact.objects.first()
    name = request.POST.get('name')
    tel = request.POST.get('tel')
    msg = request.POST.get('msg')
    product = request.POST.get('product')
    message = f'Имя: {name} \nНомер телефона: {tel} \nТовар: {product} \n\nВопрос:\n{msg}'
    em = EmailMessage(subject='Новое сообщение с сайта',
                      body=message,
                      to=[page.email],
                      headers={'content-type': 'text/html'}
                      )
    try:
        em.send()
        return JsonResponse({'status': 'ok', 'text': 'Мы получили Ваше сообщение! Вскоре наш менеджер свяжется с Вами.'})
    except:
        return JsonResponse({'status': 'bad', 'text': 'Ошибка отправки сообщения'})


