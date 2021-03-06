# Generated by Django 3.2.7 on 2021-10-09 08:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20211009_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-publish',), 'verbose_name': 'Запись', 'verbose_name_plural': 'Записи'},
        ),
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='опубликовано'),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(max_length=200, unique_for_date='publish', verbose_name='слаг'),
        ),
    ]
