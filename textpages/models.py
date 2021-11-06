from django.db import models
from django_quill.fields import QuillField


class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страница ИБ'
        verbose_name_plural = 'Страница ИБ'


class Section(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='Иконка (необязательно)', blank=True)
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = QuillField(verbose_name='Контент')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.title