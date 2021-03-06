from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Category, Delivery, Tag
from .utils import get_filters, get_prices, get_filtered_products, get_min_price, get_variation_filters, \
    get_filtered_var_products
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from reviews.forms import ReviewForm
from random import shuffle
from blog.models import Article
from config.models import Config
from django.core.mail import EmailMessage
from shop.settings import SEND_MAIL_TO
from contacts.models import Contact
from shop.settings import TITLE_SUFFIX
from django.views.decorators.cache import cache_page


def mailru(request):
    return render(request, 'catalog/mailru.html', {})


def index(request):
    articles = Article.published.all()[:12]
    top_products = Product.simple.all().order_by('-sales')[:12]
    exclude_list = list(item.id for item in top_products)
    new_products = Product.simple.exclude(pk__in=exclude_list)[:12]
    new_products_r = list(new_products)
    shuffle(new_products_r)
    config = Config.objects.first()
    banner_product = False
    title = f'Главная{TITLE_SUFFIX}'
    try:
        banner_products = list(config.main_product.all())
        if banner_products:
            shuffle(banner_products)
            banner_product = banner_products[0]
    except:
        pass

    brands = False
    try:
        brands = config.brands.all()
    except:
        pass
    context = {
        'top_products': top_products,
        'articles': articles,
        'new_products': new_products_r,
        'banner_product': banner_product,
        'brands': brands,
        'title': title
    }
    return render(request, 'catalog/index.html', context)


# @cache_page(60 * 1440)
def product_detail(request, slug):
    delivery = Delivery.objects.first()
    product = get_object_or_404(Product, slug=slug)
    variations = product.variations.all().values('pk')
    tags = None
    min_price = None
    filters = None
    if variations.count() > 0:
        product_type = 'variable'
        tags = Tag.objects.filter(products__id__in=variations).distinct()
        min_price = get_min_price(variations)
        filters = get_variation_filters(product)
    else:
        product_type = 'simple'

    title = f'{product.name}{TITLE_SUFFIX}'
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
    if parent_category:
        breadcrumbs.append({
            'label': parent_category.name,
            'url': parent_category.get_absolute_url,
            'type': 'link'
        })
    if category:
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
        try:
            kit = attribute.kit_set.get(product=product)
            product_attributes.append({
                'name': attribute.name,
                'value': kit.value
            })
        except:
            pass
    similar_products = list(Product.simple.filter(category=category).exclude(id=product.id))
    shuffle(similar_products)
    accessories_cats = product.accessories.all()
    accessories = list(Product.simple.filter(category__in=accessories_cats))
    shuffle(accessories)
    context = {
        'product': product,
        'product_attributes': product_attributes,
        'breadcrumbs': breadcrumbs,
        'review_form': review_form,
        'similar_products': similar_products[:24],
        'accessories': accessories,
        'delivery': delivery,
        'title': title,
        'product_type': product_type,
        'variations': variations,
        'min_price': min_price,
        'tags': tags,
        'filters': filters
    }
    print(variations)
    return render(request, 'catalog/single.html', context)


def product_detail_filtered(request, slug, params):
    delivery = Delivery.objects.first()
    product = get_object_or_404(Product, slug=slug)
    var_products = product.variations.all()
    tags = None
    min_price = None
    filters = None
    if var_products.count() > 0:
        product_type = 'variable'

        min_price = get_min_price(var_products)
        filters = get_variation_filters(product)
        query_filters = []
        params_list = params.split(';')
        for p in params_list:
            p_list = p.split(':')
            key = p_list[0]
            vals = p_list[1].split('=')
            query_filters.append({
                'key': key,
                'values': vals
            })
        products = get_filtered_var_products(var_products, query_filters)
        products_for_filter = products.values('pk')
        var_list_products = list(p.id for p in products)
        tags = Tag.objects.filter(products__id__in=products_for_filter).distinct()
    else:
        product_type = 'simple'

    title = f'{product.name}{TITLE_SUFFIX}'
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
    if parent_category:
        breadcrumbs.append({
            'label': parent_category.name,
            'url': parent_category.get_absolute_url,
            'type': 'link'
        })
    if category:
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
        try:
            kit = attribute.kit_set.get(product=product)
            product_attributes.append({
                'name': attribute.name,
                'value': kit.value
            })
        except:
            pass
    similar_products = list(Product.simple.filter(category=category).exclude(id=product.id))
    shuffle(similar_products)
    accessories_cats = product.accessories.all()
    accessories = list(Product.simple.filter(category__in=accessories_cats))
    shuffle(accessories)
    context = {
        'product': product,
        'product_attributes': product_attributes,
        'breadcrumbs': breadcrumbs,
        'review_form': review_form,
        'similar_products': similar_products[:24],
        'accessories': accessories,
        'delivery': delivery,
        'title': title,
        'product_type': product_type,
        'min_price': min_price,
        'tags': tags,
        'filters': filters,
        'var_list_products': var_list_products,
        'filtered': 'yes'
    }
    return render(request, 'catalog/single.html', context)


@cache_page(60 * 1440)
def products_by_cat(request, slug):
    category = get_object_or_404(Category, slug=slug)
    title = f'{category.name}{TITLE_SUFFIX}'
    children_categories = category.category_set.all()
    q = Q(category=category)
    for children_category in children_categories:
        q |= Q(category=children_category)

    products_list = Product.simple.filter(q).order_by('-sales')
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
            title = f'Результаты поиска: "{query}"{TITLE_SUFFIX}'
            context = {
                'category': category,
                'products': products_list,
                'prices': prices,
                'filters': filters,
                'search_form': form,
                'query_string': query,
                'breadcrumbs': breadcrumbs,
                'slug': slug,
                'title': title
            }

            return render(request, 'catalog/catalog.html', context)

    if request.method == 'GET':
        filters = get_filters(request, category, children_categories)
        prices = get_prices(products_list, request)

        paginator = Paginator(products_list, 12)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

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
            'search_form': form,
            'breadcrumbs': breadcrumbs,
            'slug': slug,
            'title': title
        }
        return render(request, 'catalog/catalog.html', context)


def search(request):
    if 'query' in request.GET:
        products_list = Product.simple.all()
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
            title = f'Результаты поиска: "{query}"{TITLE_SUFFIX}'
            context = {
                'products': products_list,
                'query_string': query,
                'breadcrumbs': breadcrumbs,
                'title': title
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
                      to=[SEND_MAIL_TO],
                      headers={'content-type': 'text/html'}
                      )
    try:
        em.send()
        return JsonResponse({'status': 'ok', 'text': 'Мы получили Ваше сообщение! Вскоре наш менеджер свяжется с Вами.'})
    except:
        return JsonResponse({'status': 'bad', 'text': 'Ошибка отправки сообщения'})


def products_by_attr(request, slug, params):
    category = get_object_or_404(Category, slug=slug)
    children_categories = category.category_set.all()
    q = Q(category=category)
    for children_category in children_categories:
        q |= Q(category=children_category)

    products_list = Product.simple.filter(q).order_by('-sales')

    form = SearchForm()
    query = None
    if 'query' in request.GET:
        prices = get_prices(products_list, request)
        filters = get_filters(request, category, children_categories)
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            products_list = products_list.annotate(similarity=TrigramSimilarity('name', query)) \
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
            title = f'Результаты поиска: "{query}"{TITLE_SUFFIX}'
            context = {
                'category': category,
                'products': products_list,
                'prices': prices,
                'filters': filters,
                'search_form': form,
                'query_string': query,
                'breadcrumbs': breadcrumbs,
                'slug': slug,
                'title': title
            }

            return render(request, 'catalog/catalog.html', context)

    query_filters = []
    attr_list = []
    params_list = params.split(';')
    page = 1
    order = False
    for p in params_list:
        p_list = p.split(':')
        key = p_list[0]
        vals = p_list[1].split('=')
        query_filters.append({
            'key': key,
            'values': vals
        })
        if key == 'page':
            page = int(vals[0])
        if key == 'order':
            order = vals[0]
    exclude_attrs = ['price', 'page', 'order']
    for atts in query_filters:
        if atts['key'] not in exclude_attrs:
            attr_list += atts['values']
    attr_str = ' + '.join(attr_list[:4])
    if attr_str:
        attr_str = ' ' + attr_str
    title = f'{category.name}{attr_str}{TITLE_SUFFIX}'
    extra_header = f'{category.name}{attr_str}'

    if request.is_ajax():
        if len(query_filters):
            try:
                products_list = get_filtered_products(request, products_list, query_filters)
            except:
                products_list = []
        if order == 'new':
            products_list = products_list.order_by('-created')
        elif order == 'price_asc':
            products_list = products_list.order_by('price_current')
        elif order == 'price_desc':
            products_list = products_list.order_by('-price_current')
        elif order == 'discount':
            products_list = products_list.order_by('price_sale', 'price_current')

        paginator = Paginator(products_list, 12)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        context = {
            'products': products,
            'title': title,
            'extra_header': extra_header
        }
        return render(request, 'catalog/products-list.html', context)

    if request.method == 'GET':
        filters = get_filters(request, category, children_categories)
        prices = get_prices(products_list, request)
        params_list = params.split(';')
        page = 1
        for p in params_list:
            p_list = p.split(':')
            key = p_list[0]
            vals = p_list[1].split('=')
            query_filters.append({
                'key': key,
                'values': vals
            })
            if key == 'page':
                page = int(vals[0])
        if len(query_filters):
            try:
                products_list = get_filtered_products(request, products_list, query_filters)
            except:
                products_list = []

        if order == 'new':
            products_list = products_list.order_by('-created')
        elif order == 'price_asc':
            products_list = products_list.order_by('price_current')
        elif order == 'price_desc':
            products_list = products_list.order_by('-price_current')
        elif order == 'discount':
            products_list = products_list.order_by('price_sale', 'price_current')

        paginator = Paginator(products_list, 12)
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
            'breadcrumbs': breadcrumbs,
            'slug': slug,
            'title': title,
            'extra_header': extra_header
        }
        return render(request, 'catalog/catalog.html', context)




