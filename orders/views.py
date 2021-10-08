from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .models import OrderItem
from cart.cart import Cart
from django.urls import reverse


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
            print('valid')
            order = checkout_form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
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
