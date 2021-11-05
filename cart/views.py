from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from catalog.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.urls import reverse
from django.http import JsonResponse
from shop.settings import TITLE_SUFFIX


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=int(cd['quantity']), update_quantity=cd['update'])
        if request.is_ajax:
            return JsonResponse({
                'status': 'ok',
                'cnt': len(cart)
            })
    if request.is_ajax:
        return JsonResponse({
            'status': 'bad',
            'cnt': len(cart)
        })
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    breadcrumbs = []
    title = f'Корзина{TITLE_SUFFIX}'
    breadcrumbs.append({
        'label': 'Корзина',
        'url': reverse('cart:cart_detail'),
        'type': 'text',

    })
    return render(request, 'cart/detail.html', {'cart': cart, 'breadcrumbs': breadcrumbs, 'title': title})

