from django.shortcuts import render, get_object_or_404
from catalog.models import Product
from django.http import JsonResponse
from .wishlist import Wishlist
from django.views.decorators.http import require_POST


def wishlist_detail(request):
    breadcrumbs = []
    breadcrumbs.append({
        'label': 'Избранное',
        'url': '',
        'type': 'text'
    })
    return render(request, 'wishlist/wishlist-page.html', {'breadcrumbs': breadcrumbs})


@require_POST
def wishlist_add(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('method') == 'add':
        if str(product_id) in wishlist.wishlist:
            return JsonResponse({
                'status': 'already added',
                'cnt': len(wishlist),
            })
        else:
            wishlist.add(product)
            return JsonResponse({
                'status': 'added',
                'cnt': len(wishlist)
            })
    else:
        wishlist.remove(product)
        return JsonResponse({
            'status': 'removed',
            'cnt': len(wishlist)
        })

