from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='слаг')

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
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='изображение')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
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
