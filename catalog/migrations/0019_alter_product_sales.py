# Generated by Django 3.2.7 on 2021-10-09 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_alter_product_sales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sales',
            field=models.PositiveIntegerField(editable=False, verbose_name='количество продаж'),
        ),
    ]
