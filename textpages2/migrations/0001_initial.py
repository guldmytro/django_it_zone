# Generated by Django 3.2.7 on 2021-11-06 14:11

from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Страница ИТ',
                'verbose_name_plural': 'Страница ИТ',
            },
        ),
        migrations.CreateModel(
            name='Section2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='images/%Y/%m/%d', verbose_name='Иконка (необязательно)')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('content', django_quill.fields.QuillField(verbose_name='Контент')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='textpages2.page2')),
            ],
        ),
    ]
