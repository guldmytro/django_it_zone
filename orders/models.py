from django.db import models
from catalog.models import Product

CLIENT_TYPES = (
    ('Физическое лицо', 'Физическое лицо'),
    ('Юридическое лицо', 'Юридическое лицо'),
)

SHIPPING_CHOICES = (
    ('Самовывоз со склада в Москве', 'Самовывоз со склада в Москве'),
    ('Бесплатная доставка', 'Бесплатная доставка'),
)

PAYMENT_CHOICES = (
    ('online', 'Оплата онлайн'),
    ('payment_upon', 'Оплата при получении')
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
    shipping = models.CharField(verbose_name='Доставка', choices=SHIPPING_CHOICES, max_length=200)
    payment = models.CharField(verbose_name='Способ оплаты', choices=PAYMENT_CHOICES, max_length=100)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

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


class ApiToken(models.Model):
    token = models.CharField(max_length=500, verbose_name='API-token сбербанка', help_text='Для теста можете \
    использовать токен: YRF3C5RFICWISEWFR6GJ', default='YRF3C5RFICWISEWFR6GJ', blank=True, null=True)

    def __str__(self):
        return f'{self.token}'

    class Meta:
        verbose_name = 'Токен оплаты'
        verbose_name_plural = 'Токены оплаты'









