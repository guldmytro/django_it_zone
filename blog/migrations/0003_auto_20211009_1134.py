# Generated by Django 3.2.7 on 2021-10-09 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_article_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='published',
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('published', 'Опубликовано')], default='draft', max_length=15, verbose_name='Статус'),
        ),
    ]
