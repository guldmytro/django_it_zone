# Generated by Django 3.2.7 on 2021-10-10 07:08

from django.db import migrations, models
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_alter_product_sales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', django_quill.fields.QuillField(blank=True, verbose_name='Оплата и доставка')),
            ],
            options={
                'verbose_name': 'Оплата и доставка',
                'verbose_name_plural': 'Оплата и доставка',
            },
        ),
    ]
