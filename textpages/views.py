from django.shortcuts import render
from django.http.response import Http404
from .models import Page
from shop.settings import TITLE_SUFFIX


def page(request):
    try:
        page = Page.objects.first()
    except:
        raise Http404

    if not page:
        raise Http404

    title = f'ИБ-Услуги{TITLE_SUFFIX}'
    breadcrumbs = []
    breadcrumbs.append({
        'label': 'ИБ-Услуги',
        'url': '',
        'type': 'text'
    })
    context = {
        'page': page,
        'title': title,
        'breadcrumbs': breadcrumbs
    }

    return render(request, 'security/detail.html', context)
