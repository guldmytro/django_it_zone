from django.db import models
from catalog.models import Product

CHOICES = (
    (5, 5),
    (4, 4),
    (3, 3),
    (2, 2),
    (1, 1),
)


class Review(models.Model):
    name = models.CharField(max_length=200, verbose_name='имя')
    text = models.TextField(verbose_name='отзыв')
    email = models.EmailField(verbose_name='E-mail')
    rating = models.PositiveSmallIntegerField(verbose_name='оценка', choices=CHOICES)
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.CASCADE, related_name='reviews')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='оновлено')

    def __str__(self):
        return f'{self.product.name} - {self.name}'

    class Meta:
        ordering = ('-created',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
