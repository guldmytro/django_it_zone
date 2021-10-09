from django.shortcuts import render, get_object_or_404
from .models import Article
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse


def archive_blog(request):
    posts_list = Article.published.all()
    paginator = Paginator(posts_list, 12)
    page = request.GET.get('page')
    if page:
        page = int(page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
        page = 1
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        page = int(paginator.num_pages)
    breadcrumbs = [{
        'label': 'Новости',
        'url': reverse('blog:archive_blog'),
        'type': 'link'
    }]
    context = {
        'page': page,
        'posts': posts,
        'page_name': 'Статьи',
        'post_type': 'archive',
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'blog/archive.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Article, slug=post, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    related_posts = False
    try:
        related_posts = Article.published.all().exclude(pk=post.pk).order_by('-publish')[:10]
    except:
        pass

    breadcrumbs = [{
        'label': 'Новости',
        'url': reverse('blog:archive_blog'),
        'type': 'link'
    }]

    breadcrumbs.append({
        'label': post.title,
        'url': '',
        'type': 'text'
    })

    context = {
        'post': post,
        'post_type': 'single',
        'related_posts': related_posts,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'blog/single.html', context)