from django.db import models
from django_quill.fields import QuillField
from django.urls import reverse


class Page(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=100)
    slug = models.SlugField(verbose_name='Слаг', max_length=100)
    thumbnail = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Иконка')
    content = QuillField(verbose_name='Контент')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создано')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('info:page_detail', args=[self.slug])
