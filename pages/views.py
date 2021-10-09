from django.shortcuts import render, get_object_or_404
from .models import Page


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    pages = Page.objects.all()
    breadcrumbs = [{
        'label': page.title,
        'url': '',
        'type': 'text'
    }]

    context = {
        'page': page,
        'pages': pages,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'pages/detail.html', context)
