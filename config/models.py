from django.db import models
from catalog.models import Product


class Config(models.Model):
    main_product = models.ManyToManyField(Product, verbose_name='продукт на главном экране')
    title = models.CharField(max_length=30, default='Настройки сайта', editable=False)
    header_logo = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True, verbose_name='Логотип в шапке')
    footer_logo = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True, verbose_name='Логотип в футере')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'


class Brand(models.Model):
    config = models.ForeignKey(Config, on_delete=models.CASCADE, related_name='brands')
    file = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='изображение')
    alt = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='создано')

    class Meta:
        ordering = ('created',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.file.url
