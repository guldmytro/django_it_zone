# Generated by Django 3.2.7 on 2021-10-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_product_price_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_current',
            field=models.DecimalField(blank=True, decimal_places=2, editable=False, max_digits=10, null=True, verbose_name='Текущая цена'),
        ),
    ]
