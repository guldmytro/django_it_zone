# Generated by Django 3.2.7 on 2021-10-09 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_remove_contact_phone_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='facebook',
            field=models.URLField(default='http://google.com'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='instagram',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
    ]
