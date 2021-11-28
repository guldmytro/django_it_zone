from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators
from django.urls import reverse
from django_quill.fields import QuillField
from django.utils import timezone
from urllib import request
from django.core.files.base import ContentFile
from brands.models import Brand


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='слаг')
    parent_category = models.ForeignKey('self', blank=True, null=True, verbose_name='родительска категория',
                                        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='изображение', blank=True)
    description = models.TextField(blank=True, verbose_name='описание')

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:products_by_cat', args=[self.slug])


class Attribute(models.Model):
    name = models.CharField(max_length=400, verbose_name='название')
    slug = models.SlugField(max_length=400, unique=True, verbose_name='слаг')
    public = models.BooleanField(verbose_name='публичный?', default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'атрибут'
        verbose_name_plural = 'атрибуты'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, blank=True, null=True,
                                 verbose_name='категория')
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    sku = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='слаг', unique=True)
    attributes = models.ManyToManyField(Attribute, through='Kit', through_fields=('product', 'attribute'))
    description = QuillField(verbose_name='длинное описание', null=True, blank=True)
    excerpt = models.TextField(blank=True, null=True, verbose_name='краткое описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена',
                                validators=[validators.MinValueValidator(0, 'Цена не может быть ниже нуля')], blank=True,
                                null=True)
    price_sale = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена со скидкой', blank=True,
                                     null=True,
                                     validators=[validators.MinValueValidator(0, message='Цена со скидкой не может \
                                     быть ниже нуля')])
    price_current = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Текущая цена', editable=False,
                                        blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name='в наличии')
    sales = models.PositiveIntegerField(verbose_name='количество продаж', editable=False, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменено')
    changed = models.DateTimeField(verbose_name='Изменено', default=timezone.now)
    accessories = models.ManyToManyField(Category, blank=True, verbose_name='аксесуары',
                                         help_text='Выберете категорию или несколько категорий товаров, \
                                         в которой находятся аксесуары для товара')

    class Meta:
        ordering = ('-created',)
        index_together = (('id', 'slug'),)
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name

    def clean(self):
        errors = {}
        if self.price_sale and self.price_sale > self.price:
            errors['price_sale'] = ValidationError(message='Цена со скидкой должна быть ниже обычной цены')
        if errors:
            raise ValidationError(errors)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.slug])


class Kit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='атрибут')
    value = models.CharField(max_length=400, verbose_name='значение')

    class Meta:
        verbose_name = 'атрибут'
        verbose_name_plural = 'атрибуты'

    def __str__(self):
        return self.attribute.name


class GalleryImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    file = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='изображение', blank=True, null=True)
    alt = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    image_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image_url and not self.file:
            try:
                res = request.urlopen(self.image_url)
                name = str(self.image_url).rsplit('/', 1)[1]
                image_name = f'{name}'
                self.file.save(image_name, ContentFile(res.read()))
            except:
                pass
        super(GalleryImage, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return 'Картинка'


class Delivery(models.Model):
    content = QuillField(verbose_name='Оплата и доставка', blank=True)
    title = models.CharField(verbose_name='Заголовок', blank=True, default='Оплата и доставка', editable=False,
                             max_length=40)

    class Meta:
        verbose_name = 'Оплата и доставка'
        verbose_name_plural = 'Оплата и доставка'

    def __str__(self):
        return 'Оплата и доставка'


html = {
    "delta": {
        "ops": [
            {
                "insert": 'First line. Second line'
            }
        ]
    },
    "html": '<p>First line</p><p>Second line</p>'
}

# django_quill.quill.Quill(
#     '{"delta": "{\\"ops\\":[{\\"insert\\":\\"this is a test!\\"},{\\"insert\\":\\"\\\\n\\"}]}","html":"<p>this is a test!</p>"}')


