from django.db import models


class Csv(models.Model):
    file = models.FileField(verbose_name='Файл', upload_to='csv/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.url

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Загрузка'
        verbose_name_plural = 'Загрузки'
