# Generated by Django 3.2.7 on 2021-11-11 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0037_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='name',
            field=models.CharField(max_length=400, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='slug',
            field=models.SlugField(max_length=400, unique=True, verbose_name='слаг'),
        ),
        migrations.AlterField(
            model_name='kit',
            name='value',
            field=models.CharField(max_length=400, verbose_name='значение'),
        ),
    ]
