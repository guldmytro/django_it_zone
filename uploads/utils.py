from catalog.models import Attribute
from django.contrib.sites.models import Site
from catalog.models import Product, Category, Kit, Tag
import csv
from unidecode import unidecode
from django.utils.text import slugify
from decimal import Decimal
from catalog.models import GalleryImage
from catalog.utils import html_to_quill
from brands.models import Brand


def get_csv_header():
    header = [
        'Идентификатор',
        'Заголовок *',
        'Артикул',
        'Родительский артикул (для вариации товара)',
        'Цена *',
        'Цена со скидкой',
        'В наличии',
        'Количество продаж *',
        'Слаг Категории *',
        'Категория *',
        'Группа (для вариации товара)',
        'Аксесуары',
        'Краткое описание',
        'Длинное описание',
        'Схемы лицензирования (для вариативного товара)',
        'Картинки *',
        'Вендор'
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
        cat_slug = product.category.slug
    except:
        cat_name = ''
        cat_slug = ''
    parent_sku = ''
    try:
        if product.parent:
            parent_sku = product.parent.sku
    except:
        pass
    brand = ''
    try:
        brand = product.brand.title
    except:
        pass
    row = [
        product.pk,
        product.name,
        product.sku,
        parent_sku,
        product.price,
        product.price_sale,
        product.available,
        product.sales,
        cat_slug,
        cat_name,
        product.tag,
        accessories,
        product.excerpt,
        product.description.html,
        product.licence_schemes.html,
        images,
        brand
    ]
    row = row + attributes_values
    return row


def push_products(csv_file, request):
    file = open(csv_file)
    csvreader = csv.reader(file)
    header = next(csvreader)
    attributes_list = header[17:]
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
        # try:
        #     update_product(product, row, attributes_list)
        # except:
        #     product.delete()
            
    file.close()


def update_product(product, row, attributes_list):
    product.name = row[1]
    product.save()
    product.sku = row[2]
    if row[4]:
        product.price = Decimal(row[4])
    if row[5]:
        product.price_sale = Decimal(row[5])

    if product.price_sale:
        product.price_current = product.price_sale
    else:
        product.price_current = product.price
    product.available = True
    product.sales = row[7]
    category_slug = row[8]
    category_str = row[9]
    try:
        category = Category.objects.get(slug=category_slug)
        product.category = category
    except:
        if category_str and category_slug:
            cat = add_category(category_str, category_slug)
            if cat:
                product.category = cat

    related_cats = str(row[11]).split(', ')
    product.accessories.clear()
    if related_cats:
        for category_str in related_cats:
            cat_slug = slugify(unidecode(category_str))
            try:
                category = Category.objects.get(slug=cat_slug)
                product.accessories.add(category)
            except:
                if category_str:
                    cat = add_category(category_str, cat_slug)
                    if cat:
                        product.accessories.add(cat)
    product.excerpt = row[12]
    try:
        product.description = html_to_quill(row[13])
    except:
        pass
    try:
        product.licence_schemes = html_to_quill(row[14])
    except:
        pass
    images_array = str(row[15]).split(', ')
    if images_array:
        update_images(images_array, product)

    product.attributes.clear()
    brand_str = row[16]
    brand_slug = slugify(unidecode(brand_str))
    if brand_slug:
        try:
            brand = Brand.objects.get(slug=brand_slug)
            product.brand = brand
        except:
            if brand_str and brand_slug:
                brand = Brand()
                brand.slug = brand_slug
                brand.title = brand_str
                brand.save()
                if brand:
                    product.brand = brand
    if attributes_list:
        for index, attribute_key in enumerate(attributes_list):
            try:
                attribute_value = str(row[17 + index])
                is_public = True
                if '*' in attribute_key:
                    is_public = False

                cd_attribute_key = attribute_key.strip().replace('*', '')
                cd_attribute_slug = slugify(unidecode(cd_attribute_key))
                if len(attribute_value) > 0:
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
            except:
                pass
    if row[3]:
        try:
            related_product = Product.objects.get(sku=row[3])
            product.parent = related_product
        except:
            pass
    if row[10]:
        try:
            group, created = Tag.objects.get_or_create(name=row[10])
            if group:
                product.tag = group
        except:
            pass
    product.save()


def add_category(category_str, cat_slug):
    cat = Category()
    cat.name = category_str
    cat.slug = cat_slug
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



