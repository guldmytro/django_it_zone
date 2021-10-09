from django.db import models
from django.urls import reverse


class Contact(models.Model):
    phone_1 = models.CharField(max_length=20, verbose_name='телефон 1')
    email = models.EmailField(verbose_name='E-mail')
    address = models.TextField(verbose_name='Адрес')
    map = models.TextField(verbose_name='iframe карты')
    schedule = models.CharField(max_length=200, verbose_name='График работы')
    facebook = models.URLField()
    instagram = models.URLField()

    def __str__(self):
        return 'Контакты'

    def get_absolute_url(self):
        return reverse('contacts:page')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'



