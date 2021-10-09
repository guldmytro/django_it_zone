from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .forms import OrderCreateForm
from .models import OrderItem, Order
from cart.cart import Cart
from django.urls import reverse
from catalog.models import Product
from django.db.models import F
import json

def order_create(request):
    cart = Cart(request)
    if len(cart) < 1:
        return redirect('cart:cart_detail')
    breadcrumbs = []
    breadcrumbs.append({
        'label': 'Корзина',
        'url': reverse('cart:cart_detail'),
        'type': 'link'
    })
    breadcrumbs.append({
        'label': 'Оформление заказа',
        'url': reverse('orders:checkout'),
        'type': 'text'
    })
    if request.method == 'POST':
        checkout_form = OrderCreateForm(request.POST)
        if checkout_form.is_valid():
            order = checkout_form.save()
            for item in cart.cart:
                product = Product.objects.get(pk=str(item))
                f = F('sales')
                product.sales = f + int(cart.cart[str(item)]['quantity'])
                product.save()
                OrderItem.objects.create(order=order, product=product, price=cart.cart[str(item)]['price'],
                                         quantity=cart.cart[str(item)]['quantity'])
            cart.clear()
            if order.payment == 'online':
                return redirect('orders:pay', id=order.pk)
            else:
                return render(request, 'orders/created.html', {'order': order})
        else:
            checkout_form = OrderCreateForm(request.POST)
            context = {
                'checkout_form': checkout_form,
                'cart': cart,
                'breadcrumbs': breadcrumbs,
                'submit_text': 'Заказ подтверждаю'
            }
            return render(request, 'orders/checkout.html', context)

    else:
        checkout_form = OrderCreateForm()
        context = {
            'checkout_form': checkout_form,
            'cart': cart,
            'breadcrumbs': breadcrumbs,
            'submit_text': 'Заказ подтверждаю'
        }
        return render(request, 'orders/checkout.html', context)


def order_pay(request, id):
    order = get_object_or_404(Order, pk=id)
    order_items = OrderItem.objects.filter(order=order)
    total_amount = int(sum(item.price * item.quantity for item in order_items))
    if order.payment != 'online' or order.paid:
        raise Http404
    context = {
        'order': order,
        'order_items': order_items,
        'total_amount': total_amount
    }
    return render(request, 'orders/pay.html', context)


def order_complete(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        order = Order.objects.get(pk=body['order_id'])
        order.paid = True
        order.save()
