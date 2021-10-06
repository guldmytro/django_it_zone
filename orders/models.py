from django.db import models
from catalog.models import Product

CLIENT_TYPES = (
    ('Физическое лицо', 'Юридическое лицо'),
    ('Юридическое', 'Физическое лицо'),
)


class Order(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    client_type = models.CharField(max_length=30, choices=CLIENT_TYPES, verbose_name='Тип клиента')
    email = models.EmailField(verbose_name='E-mail')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    paid = models.BooleanField(default=False, verbose_name='Оплачено')
    comment = models.TextField(verbose_name='Комментарий к заказу', blank=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Заказ {self.pk}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.pk}'

    def get_cost(self):
        return self.price * self.quantity