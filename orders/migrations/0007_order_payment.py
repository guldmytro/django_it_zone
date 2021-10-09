# Generated by Django 3.2.7 on 2021-10-09 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('online', 'Оплата онлайн'), ('payment_upon', 'Оплата при получении')], default=0, max_length=100, verbose_name='Способ оплаты'),
            preserve_default=False,
        ),
    ]
