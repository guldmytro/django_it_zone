from .models import Kit, Attribute
from django.db.models import Count, Q
from django.template.defaultfilters import slugify


def get_filters(category):
    result = []

    for attribute in Attribute.objects.filter(Q(product__category=category)).distinct():
        attribute_dict = {
            'name': attribute.name,
            'values': {}
        }
        for kit in Kit.objects.filter(attribute=attribute).annotate(cnt=Count('product',
                                                                              filter=Q(product__category=category))):
            slug = slugify(kit.value)
            if slug in attribute_dict['values']:
                attribute_dict['values'][slug]['cnt'] += kit.cnt
            else:
                attribute_dict['values'][slug] = {
                    'value': kit.value,
                    'slug': slug,
                    'cnt': kit.cnt,
                }

        result.append(attribute_dict)

    return result
