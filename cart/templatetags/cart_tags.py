from django import template
from decimal import Decimal

register = template.Library()


@register.simple_tag
def cart_quantity(cart, id):
    quantity = cart[str(id)]['quantity']
    return quantity


@register.simple_tag
def cart_subtotal(cart, id):
    item = cart[str(id)]
    subtotal = int(int(item['quantity']) * Decimal(item['price']))
    return subtotal
