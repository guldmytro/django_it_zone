from django.shortcuts import render, get_object_or_404
from .models import Page
from shop.settings import TITLE_SUFFIX


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.all()
    title = f'{page.title}{TITLE_SUFFIX}'
    breadcrumbs = [{
        'label': page.title,
        'url': '',
        'type': 'text',
    }]

    context = {
        'page': page,
        'pages': pages,
        'breadcrumbs': breadcrumbs,
        'title': title
    }
    return render(request, 'pages/detail.html', context)
