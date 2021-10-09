from django.db import models
from django_quill.fields import QuillField
from django.utils import timezone
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    )
    title = models.CharField(max_length=200, verbose_name='заголовок')
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='слаг', unique_for_date='publish')
    excerpt = models.TextField(verbose_name='краткое описание')
    content = QuillField(verbose_name='Описание', blank=True, null=True)
    thumbnail_1 = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='изображение записи', blank=True)
    thumbnail_2 = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='изображение записи', blank=True)
    publish = models.DateTimeField(verbose_name="опубликовано", default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменено')
    status = models.CharField(verbose_name="Статус", max_length=15, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])
