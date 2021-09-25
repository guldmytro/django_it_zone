from django.db import models
from django.core.exceptions import ValidationError
from django.core import validators


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='слаг')
    parent_category = models.ForeignKey('self', blank=True, verbose_name='родительска категория',
                                        on_delete=models.CASCADE)
    description = models.TextField(blank=True, verbose_name='описание')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='изображение')

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='слаг')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='изображение')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена',
                                validators=[validators.MinValueValidator(0, 'Цена не может быть ниже нуля')])
    price_sale = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена со скидкой', blank=True,
                                     validators=[validators.MinValueValidator(0, message='Цена со скидкой не может \
                                     быть ниже нуля')])
    available = models.BooleanField(default=True, verbose_name='в наличии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменено')

    class Meta:
        ordering = ('-updated',)
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
