from django.db import models
from django_quill.fields import QuillField
from django.urls import reverse


class Brand(models.Model):
    title = models.CharField(max_length=300, verbose_name='заголовок')
    slug = models.SlugField(max_length=300, db_index=True, verbose_name='слаг', unique=True)
    content = QuillField(blank=True, verbose_name='контент')
    image = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='изображение', blank=True, null=True)
    certificate = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='сертификат', blank=True, null=True)
    top = models.BooleanField(default=False, verbose_name='в топе', blank=True, null=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'

    def get_absolute_url(self):
        return reverse('brands:detail', args=[self.slug])

    def __str__(self):
        return self.title