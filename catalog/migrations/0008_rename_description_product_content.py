# Generated by Django 3.2.7 on 2021-09-26 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_product_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='content',
        ),
    ]
