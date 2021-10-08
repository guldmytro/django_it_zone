# Generated by Django 3.2.7 on 2021-10-07 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client_type',
            field=models.CharField(choices=[('Физическое лицо', 'Юридическое лицо'), ('Юридическое лицо', 'Физическое лицо')], max_length=30, verbose_name='Тип клиента'),
        ),
    ]
