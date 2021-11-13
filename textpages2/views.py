from django.shortcuts import render
from django.http.response import Http404
from .models import Page2
from shop.settings import TITLE_SUFFIX


def page(request):
    try:
        page = Page2.objects.first()
    except:
        raise Http404

    if not page:
        raise Http404

    breadcrumbs = []
    breadcrumbs.append({
        'label': 'СКУД',
        'url': '',
        'type': 'text'
    })
    title = f'ИТ-Услуги{TITLE_SUFFIX}'
    context = {
        'page': page,
        'title': title,
        'breadcrumbs': breadcrumbs
    }

    return render(request, 'it/detail.html', context)
