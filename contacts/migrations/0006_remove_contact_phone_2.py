# Generated by Django 3.2.7 on 2021-10-09 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_alter_contact_phone_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='phone_2',
        ),
    ]
