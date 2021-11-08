from catalog.models import Attribute
from django.contrib.sites.models import Site
from catalog.models import Product, Category, Kit
import csv
from unidecode import unidecode
from django.utils.text import slugify
from decimal import Decimal
from catalog.models import GalleryImage
from catalog.utils import html_to_quill


def get_csv_header():
    header = [
        'Идентификатор',
        'Заголовок *',
        'Артикул',
        'Цена *',
        'Цена со скидкой',
        'В наличии',
        'Количество продаж *',
        'Категория *',
        'Аксесуары',
        'Краткое описание',
        'Длинное описание',
        'Картинки *',
    ]
    return header


def get_attributes_header():
    attributes = Attribute.objects.all()
    attr_header = []
    for item in attributes:
        if item.public:
            name = item.name
        else:
            name = f'{item.name}*'
        attr_header.append(name)
    return attr_header


def get_product_row(product, attributes, request):
    accessories = list(item.name for item in product.accessories.all())
    accessories = ', '.join(accessories)
    site = Site.objects.get_current()
    prefix = f'{request.scheme}://{site.domain}'
    try:
        images = list(f'{prefix}{item.file.url}' for item in product.images.all())
        images = ', '.join(images)
    except:
        images = ''
    attributes_values = []
    for attribute in attributes:
        try:
            kit = attribute.kit_set.get(product=product)
            attributes_values.append(kit.value)
        except:
            attributes_values.append('')
    try:
        cat_name = product.category.name
    except:
        cat_name = ''
    row = [
        product.pk,
        product.name,
        product.sku,
        product.price,
        product.price_sale,
        product.available,
        product.sales,
        cat_name,
        accessories,
        product.excerpt,
        product.description.html,
        images
    ]
    row = row + attributes_values
    return row


def push_products(csv_file, request):
    file = open(csv_file)
    csvreader = csv.reader(file)
    header = next(csvreader)
    attributes_list = header[12:]
    rows = []
    for row in csvreader:
        rows.append(row)
    for row in rows:
        slug = slugify(unidecode(row[1]))
        try:
            product = Product.objects.get(slug=slug)
        except:
            product = Product()
            product.slug = slug
            product.save()


        update_product(product, row, attributes_list)
        # product.delete()
    file.close()


def update_product(product, row, attributes_list):
    product.name = row[1]
    product.save()
    product.sku = row[2]
    product.price = Decimal(row[3])
    if row[4]:
        product.price_sale = Decimal(row[4])
    product.save()
    if product.price_sale:
        product.price_current = product.price_sale
    else:
        product.price_current = product.price
    product.save()
    product.available = True
    product.sales = row[6]
    category_str = row[7]
    product.save()
    try:
        category = Category.objects.get(name=category_str)
        product.category = category
    except:
        if category_str:
            cat = add_category(category_str)
            if cat:
                product.category = cat

    related_cats = str(row[8]).split(', ')
    product.accessories.clear()
    if related_cats:
        for category_str in related_cats:
            try:
                category = Category.objects.get(name=category_str)
                product.accessories.add(category)
            except:
                if category_str:
                    cat = add_category(category_str)
                    if cat:
                        product.accessories.add(cat)
    product.excerpt = row[9]
    try:
        product.description = html_to_quill(row[10])
    except:
        pass
    images_array = str(row[11]).split(', ')
    if images_array:
        update_images(images_array, product)

    product.attributes.clear()
    if attributes_list:
        for index, attribute_key in enumerate(attributes_list):
            attribute_value = str(row[12 + index])
            is_public = True
            if '*' in attribute_key:
                is_public = False

            cd_attribute_key = attribute_key.strip().replace('*', '')
            cd_attribute_slug = slugify(unidecode(cd_attribute_key))
            if attribute_value:
                try:
                    attribute = Attribute.objects.get(slug=cd_attribute_slug)
                    attribute.public = is_public
                    attribute.save()
                except:
                    attribute = Attribute()
                    attribute.name = cd_attribute_key
                    attribute.slug = cd_attribute_slug
                    attribute.public = is_public
                    attribute.save()
                Kit.objects.create(attribute=attribute, product=product, value=attribute_value)

    product.save()


def add_product():
    pass


def add_category(category_str):
    cat = Category()
    cat.name = category_str
    cat.slug = slugify(unidecode(category_str))
    cat.save()
    return cat


def update_images(images_array, product):
    GalleryImage.objects.filter(product=product).update(product=None)
    for url in images_array:
        try:
            image = GalleryImage()
            image.product = product
            image.image_url = url
            image.save()
        except:
            pass



