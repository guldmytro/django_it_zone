# Generated by Django 3.2.7 on 2021-10-08 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)], verbose_name='оценка'),
        ),
    ]
