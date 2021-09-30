from django import template

register = template.Library()


@register.filter
def min_price(price):
    price = round(int(price) * 0.9 / 1000) * 1000
    return price


@register.filter
def max_price(price):
    price = round(int(price) * 1.1 / 1000) * 1000
    return price
