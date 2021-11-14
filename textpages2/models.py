from django.db import models
from django_quill.fields import QuillField


class Page2(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страница ИТ-Услуг'
        verbose_name_plural = 'Страница ИТ-услуг'
        ordering = ['id']


class Section2(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = QuillField(verbose_name='Контент')
    page = models.ForeignKey(Page2, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['pk']