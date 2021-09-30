from .models import Kit, Attribute
from django.db.models import Count, Q, Min, Max
from django.template.defaultfilters import slugify


def get_filters(request, category):
    result = []
    for attribute in Attribute.objects.filter(Q(product__category=category)).distinct():
        attribute_dict = {
            'name': attribute.name,
            'slug': attribute.slug,
            'values': []
        }
        for kit in Kit.objects.filter(attribute=attribute).annotate(cnt=Count('product',
                                                                              filter=Q(product__category=category))):
            slug = slugify(kit.value)
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
    result = {
        'min': result['min_price'],
        'max': result['max_price']
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
        elif query_filter['key'] == 'csrfmiddlewaretoken':
            pass
        else:
            key = query_filter['key']
            attribute = Attribute.objects.get(slug=key)
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
        elif query_filter['key'] == 'csrfmiddlewaretoken':
            pass
        else:
            key = query_filter['key']
            attribute = Attribute.objects.get(slug=key)
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
