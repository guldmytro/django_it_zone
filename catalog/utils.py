from .models import Kit, Attribute
from django.db.models import Count, Q, Min, Max
from django.utils.text import slugify


def get_filters(request, category, children_categories):
    result = []
    q = Q(product__category=category)
    for children_category in children_categories:
        q |= Q(product__category=children_category)

    for attribute in Attribute.objects.filter(q).distinct():
        attribute_dict = {
            'name': attribute.name,
            'slug': attribute.slug,
            'values': []
        }
        for kit in Kit.objects.filter(attribute=attribute).annotate(cnt=Count('product',
                                                                              filter=q)):
            slug = slugify(kit.value, allow_unicode=True)
            found = False
            for filter in attribute_dict['values']:
                if filter['slug'] == slug:
                    filter['cnt'] += 1
                    found = True
                    break

            if not found:
                get_parameters = request.GET.getlist(attribute.slug)
                if kit.value in get_parameters:
                    checked = True
                else:
                    checked = False
                if kit.cnt > 0:
                    attribute_dict['values'].append({
                        'value': kit.value,
                        'slug': slug,
                        'cnt': kit.cnt,
                        'checked': checked
                    })
        result.append(attribute_dict)
    return result


def get_prices(products, request):
    result = products.aggregate(min_price=Min('price_current'), max_price=Max('price_current'))
    try:
        result = {
            'min': int(result['min_price']),
            'max': int(result['max_price'])
        }
    except:
        result = {
            'min': 0,
            'max': 0
        }

    if request.GET.get('price'):
        prices = parse_price(request.GET.get('price'))
        result['current_min'] = prices['min']
        result['current_max'] = prices['max']

    return result


def get_filtered_products(request, products, query_filters):
    for query_filter in query_filters:
        if query_filter['key'] == 'price':
            prices = parse_price(request.GET.get('price'))
            products = products.filter(price_current__gte=prices['min'], price_current__lte=prices['max'])
        else:
            key = query_filter['key']
            try:
                attribute = Attribute.objects.get(slug=key)
            except:
                continue
            values = query_filter['values']
            q = Q()
            for value in values:
                # q |= Q(**{param__key: param_value})
                q |= (Q(kit__value=value) & Q(kit__attribute=attribute))
            products = products.filter(q)
    return products


def get_filtered_products_p(request, products, query_filters):
    for query_filter in query_filters:
        if query_filter['key'] == 'price':
            prices = parse_price(query_filter['values'][0])
            products = products.filter(price_current__gte=prices['min'], price_current__lte=prices['max'])
        else:
            key = query_filter['key']
            try:
                attribute = Attribute.objects.get(slug=key)
            except:
                continue
            values = query_filter['values']
            q = Q()
            for value in values:
                # q |= Q(**{param__key: param_value})
                q |= (Q(kit__value=value) & Q(kit__attribute=attribute))
            products = products.filter(q)
    return products


def parse_price(price):
    prices = price.split(';')
    prices = [int(i) for i in prices]
    result = {
        'min': min(prices),
        'max': max(prices)
    }
    return result


def get_page_from_query(query):
    for query_filter in query:
        if query_filter['key'] == 'page':
            return query_filter['values'][0]


def get_full_path_from_query(query):
    for query_filter in query:
        if query_filter['key'] == 'full_path':
            return query_filter['values'][0]
