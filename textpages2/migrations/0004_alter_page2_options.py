# Generated by Django 3.2.7 on 2021-11-06 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textpages2', '0003_auto_20211106_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page2',
            options={'ordering': ['-pk'], 'verbose_name': 'Страница ИТ', 'verbose_name_plural': 'Страница ИТ'},
        ),
    ]
