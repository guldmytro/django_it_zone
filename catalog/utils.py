# import json

from .models import Kit, Attribute
from django.db.models import Count, Q, Min, Max
# from django.utils.text import slugify
from django_quill.quill import Quill
from django.utils.html import strip_tags


def get_filters(request, category, children_categories):
    result = []
    cats = [category.name]
    q = Q(product__category=category)
    for children_category in children_categories:
        cats.append(children_category.name)
        q |= Q(product__category=children_category)

    for attribute in Attribute.objects.filter(public=True).filter(q).distinct():
        attribute_dict = {
            'name': attribute.name,
            # 'slug': attribute.slug,
            'values': []
        }
        appended_values = []
        for kit in Kit.objects.filter(attribute=attribute).annotate(cnt=Count('product',
                                                                              filter=q)).distinct():
            # slug = slugify(kit.value, allow_unicode=True)
            # found = False

            if kit.cnt > 0 and kit.product.category.name in cats and kit.value not in appended_values:
                attribute_dict['values'].append({
                    'value': kit.value,
                })
                appended_values.append(kit.value)
            #
            # for filter in attribute_dict['values']:
            #     try:
            #         if filter['slug'] == slug and kit.product.category.name in cats:
            #             filter['cnt'] += 1
            #             found = True
            #             break
            #     except:
            #         pass
            #
            # if not found:
            #     if kit.cnt > 0 and kit.product.category.name in cats:
            #         attribute_dict['values'].append({
            #             'value': kit.value,
            #             'slug': slug,
            #             'cnt': kit.cnt
            #         })
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
            prices = parse_price(query_filter['values'])
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


def parse_price(prices):
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


def html_to_quill(html):
    text = strip_tags(html)
    # quill = Quill('{"delta":"{\\"ops\\":[{\\"insert\\":\\"this is a test!\\"},{\\"insert\\":\\"\\\\n\\"}]}","html":"<p>this is a test!</p>"}')
    quill = Quill('{"delta":"{\\"ops\\":[{\\"insert\\":\\"' + text + '\\"},{\\"insert\\":\\"\\\\n\\"}]}","html":"' + html + '"}')
    return quill


from .models import Product


def test():
    p = Product.objects.get(pk=45)
    q = html_to_quill('Some Test without tags')
    p.description = q
    p.save()
