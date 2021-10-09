# Generated by Django 3.2.7 on 2021-10-09 08:22

from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='заголовок')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='слаг')),
                ('excerpt', models.TextField(verbose_name='краткое описание')),
                ('content', django_quill.fields.QuillField(blank=True, null=True, verbose_name='Описание')),
                ('thumbnail_1', models.ImageField(blank=True, upload_to='images/%Y/%m/%d', verbose_name='изображение записи')),
                ('thumbnail_2', models.ImageField(blank=True, upload_to='images/%Y/%m/%d', verbose_name='изображение записи')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='изменено')),
            ],
            options={
                'verbose_name': 'статья',
                'verbose_name_plural': 'статьи',
                'ordering': ('-created',),
            },
        ),
    ]
