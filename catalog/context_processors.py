from .models import Category
from .forms import SearchForm
from config.models import Config


def menu_catalog_processor(request):
    categories = []
    parent_cats = Category.objects.filter(parent_category=None)
    for category in parent_cats:
        category_dict = {
            'category': category,
            'childrens': []
        }
        child_categories = Category.objects.filter(parent_category=category)
        category_dict['childrens'] = list(child_categories)
        categories.append(category_dict)
    return {'categories': categories}


def search_form(request):
    if request.GET.get('query'):
        global_form = SearchForm(initial={'query': request.GET.get('query')})
    else:
        global_form = SearchForm()
    return {'global_form': global_form}


def logos(request):
    try:
        config = Config.objects.first()
        context = {
            'header_logo': config.header_logo,
            'footer_logo': config.footer_logo
        }
        return context
    except:
        return {}
