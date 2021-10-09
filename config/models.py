from django.db import models
from catalog.models import Product


class Config(models.Model):
    main_product = models.ManyToManyField(Product, verbose_name='продукт на главном экране')
    title = models.CharField(max_length=30, default='Настройки сайта', editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'
