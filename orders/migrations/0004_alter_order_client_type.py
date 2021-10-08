# Generated by Django 3.2.7 on 2021-10-07 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_client_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='client_type',
            field=models.CharField(choices=[('Физическое лицо', 'Физическое лицо'), ('Юридическое лицо', 'Юридическое лицо')], max_length=30, verbose_name='Тип клиента'),
        ),
    ]
