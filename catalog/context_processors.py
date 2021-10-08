from .models import Category


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
