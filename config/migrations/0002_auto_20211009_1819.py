# Generated by Django 3.2.7 on 2021-10-09 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_alter_product_accessories'),
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='config',
            options={'verbose_name': 'Настройки', 'verbose_name_plural': 'Настройки'},
        ),
        migrations.AlterField(
            model_name='config',
            name='main_product',
            field=models.ManyToManyField(to='catalog.Product', verbose_name='продукт на главном экране'),
        ),
    ]
